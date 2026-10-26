"""Ayush owns orchestration and the CLI; the detector is replaceable via Protocol."""

import hashlib
import json
import platform
import shutil
import tempfile
from collections.abc import Callable, Iterable, Iterator
from dataclasses import asdict
from pathlib import Path
from time import perf_counter_ns
from typing import Any

from sentinel import __version__
from sentinel.config import DetectorConfig
from sentinel.contracts import (
    SCHEMA_VERSION,
    ContractError,
    Detector,
    EvaluationScope,
    Observation,
    Prediction,
    timestamp_text,
)
from sentinel.data.io import read_observations
from sentinel.detectors.rolling import RollingMADStarter


def process_stream(
    observations: Iterable[Observation], factory: Callable[[], Detector], max_series: int = 100
) -> Iterator[tuple[Prediction, int]]:
    detectors: dict[str, Detector] = {}
    for observation in observations:
        if observation.series_id not in detectors:
            if len(detectors) >= max_series:
                raise ContractError("Maximum active series exceeded")
            detectors[observation.series_id] = factory()
        start = perf_counter_ns()
        prediction = detectors[observation.series_id].process(observation)
        yield prediction, perf_counter_ns() - start


def prediction_record(prediction: Prediction, elapsed_ns: int) -> dict[str, Any]:
    payload = asdict(prediction)
    payload["timestamp"] = timestamp_text(prediction.timestamp)
    payload["schema_version"] = SCHEMA_VERSION
    payload["elapsed_ns"] = elapsed_ns
    return payload


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def run_file(
    input_path: Path,
    output_dir: Path,
    config: DetectorConfig,
    scope: EvaluationScope,
    dataset_id: str,
) -> dict[str, Any]:
    if scope not in ("synthetic_smoke", "development_validation"):
        raise ContractError("Starter supports synthetic_smoke or development_validation only")
    if not dataset_id.strip():
        raise ContractError("dataset_id is required")
    if output_dir.exists():
        raise ContractError(
            f"Output directory already exists: {output_dir}; use a new run directory"
        )
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".sentinel-", dir=output_dir.parent))
    try:
        count = ready_count = alerts = total_ns = 0
        with (temporary / "predictions.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
            for prediction, elapsed in process_stream(
                read_observations(input_path),
                lambda: RollingMADStarter(config),
                config.max_series,
            ):
                stream.write(
                    json.dumps(prediction_record(prediction, elapsed), allow_nan=False) + "\n"
                )
                count += 1
                ready_count += int(prediction.ready)
                alerts += int(prediction.label == "ANOMALOUS")
                total_ns += elapsed
        metadata = {
            "schema_version": SCHEMA_VERSION,
            "package_version": __version__,
            "algorithm": "rolling_mad_starter",
            "evaluation_scope": scope,
            "dataset_id": dataset_id,
            "input_sha256": sha256_file(input_path),
            "predictions_sha256": sha256_file(temporary / "predictions.jsonl"),
            "config": config.to_dict(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "observations": count,
            "ready_observations": ready_count,
            "anomalous_points": alerts,
            "detector_total_ns": total_ns,
            "runtime_note": (
                "process() only, includes warmup; excludes parsing/writing; not a benchmark"
            ),
            "official_submission_ready": False,
        }
        (temporary / "run.json").write_text(
            json.dumps(metadata, indent=2, allow_nan=False) + "\n", encoding="utf-8", newline="\n"
        )
        temporary.rename(output_dir)
        return metadata
    except BaseException:
        shutil.rmtree(temporary)
        raise
