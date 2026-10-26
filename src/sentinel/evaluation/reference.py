"""Provisional event-trigger F1 v0. See docs/EVALUATION.md before interpreting."""

import json
from collections import defaultdict
from collections.abc import Iterable
from math import isfinite
from pathlib import Path
from typing import Any

from sentinel.contracts import AnomalyWindow, ContractError, parse_timestamp
from sentinel.data.io import read_windows
from sentinel.pipeline import sha256_file


def event_metrics(
    records: Iterable[dict[str, Any]], windows: list[AnomalyWindow]
) -> dict[str, Any]:
    grouped: dict[str, list[AnomalyWindow]] = defaultdict(list)
    for window in windows:
        grouped[window.series_id].append(window)
    for items in grouped.values():
        items.sort(key=lambda item: item.start)
        for previous, current in zip(items, items[1:], strict=False):
            if current.start <= previous.end:
                raise ContractError("Overlapping/touching closed truth windows are ambiguous")

    matched: set[tuple[str, int]] = set()
    active: dict[str, bool] = {}
    last_time: dict[str, Any] = {}
    first_time: dict[str, Any] = {}
    delays: list[float] = []
    tp = fp = warmup_count = count = 0
    for record in records:
        try:
            series = record["series_id"]
            if not isinstance(series, str) or not series.strip():
                raise ContractError("Invalid series_id")
            timestamp = parse_timestamp(record["timestamp"])
            if series in last_time and timestamp <= last_time[series]:
                raise ContractError("Prediction timestamps must increase within each series")
            first_time.setdefault(series, timestamp)
            last_time[series] = timestamp
            if record["schema_version"] != "1.0":
                raise ContractError("Unsupported prediction schema")
            ready = record["ready"]
            if type(ready) is not bool:
                raise ContractError("ready must be boolean")
            score, threshold = record["score"], record["threshold"]
            if type(threshold) not in (int, float) or not isfinite(threshold) or threshold <= 0:
                raise ContractError("Invalid threshold")
            if ready:
                if type(score) not in (int, float) or not isfinite(score) or score < 0:
                    raise ContractError("Ready score must be finite and nonnegative")
                expected = "ANOMALOUS" if score >= threshold else "NORMAL"
            else:
                if score is not None:
                    raise ContractError("Warmup score must be null")
                expected = "NORMAL"
                warmup_count += 1
            if record["label"] != expected:
                raise ContractError("Label contradicts score/threshold/readiness")
            flagged = record["label"] == "ANOMALOUS"
        except (KeyError, TypeError) as exc:
            raise ContractError(f"Malformed prediction record: {exc}") from exc
        count += 1
        if flagged and not active.get(series, False):
            found = next(
                (
                    index
                    for index, window in enumerate(grouped.get(series, []))
                    if window.start <= timestamp <= window.end and (series, index) not in matched
                ),
                None,
            )
            if found is None:
                fp += 1
            else:
                matched.add((series, found))
                tp += 1
                delays.append((timestamp - grouped[series][found].start).total_seconds())
        active[series] = flagged

    if not count:
        raise ContractError("Predictions are empty")
    for window in windows:
        if (
            window.series_id not in last_time
            or window.start < first_time[window.series_id]
            or window.end > last_time[window.series_id]
        ):
            raise ContractError("Truth window lies outside prediction coverage")
    fn = len(windows) - tp
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0
    return {
        "metric_id": "provisional_event_trigger_f1_v0",
        "official_metric": False,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "event_f1": f1,
        "delay_seconds": delays,
        "mean_delay_seconds": sum(delays) / len(delays) if delays else None,
        "warmup_points_included_in_coverage": warmup_count,
        "observations": count,
    }


def evaluate_run(run_dir: Path, windows_path: Path) -> dict[str, Any]:
    metadata = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    if metadata.get("evaluation_scope") not in ("synthetic_smoke", "development_validation"):
        raise ContractError("Unsupported scope; official scoring adapter is not implemented")
    predictions_path = run_dir / "predictions.jsonl"
    if metadata.get("predictions_sha256") != sha256_file(predictions_path):
        raise ContractError("Predictions checksum differs from run manifest")
    with predictions_path.open(encoding="utf-8") as stream:
        result = event_metrics((json.loads(line) for line in stream), read_windows(windows_path))
    return {
        **result,
        "evaluation_scope": metadata["evaluation_scope"],
        "dataset_id": metadata["dataset_id"],
        "input_sha256": metadata["input_sha256"],
        "windows_sha256": sha256_file(windows_path),
    }
