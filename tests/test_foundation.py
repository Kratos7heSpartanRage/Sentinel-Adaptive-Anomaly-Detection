import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from sentinel.cli import main
from sentinel.config import DetectorConfig, load_config
from sentinel.contracts import AnomalyWindow, ContractError, Observation, parse_timestamp
from sentinel.data.io import read_observations
from sentinel.detectors.rolling import RollingMADStarter
from sentinel.evaluation.reference import evaluate_run, event_metrics
from sentinel.pipeline import prediction_record, process_stream, run_file

FIXTURES = Path(__file__).parent / "fixtures"


def observation(index: int, value: float = 10.0, series: str = "s") -> Observation:
    return Observation(series, parse_timestamp(f"2026-01-01T00:{index:02d}:00Z"), value)


def record(index: int, flag: bool = False, series: str = "s") -> dict[str, Any]:
    detector = RollingMADStarter(DetectorConfig(min_history=2))
    detector.process(observation(0, series=series))
    detector.process(observation(1, series=series))
    result = detector.process(observation(index, 12.0 if flag else 10.0, series))
    return prediction_record(result, 0)


def window(start: int, end: int, series: str = "s") -> AnomalyWindow:
    return AnomalyWindow(series, observation(start).timestamp, observation(end).timestamp)


def test_warmup_and_score_before_update() -> None:
    detector = RollingMADStarter(DetectorConfig(min_history=2))
    assert detector.process(observation(0)).score is None
    assert not detector.process(observation(1)).ready
    result = detector.process(observation(2, 12.0))
    assert result.label == "ANOMALOUS"
    assert result.evidence.baseline == 10.0
    assert result.evidence.history_size == 2
    assert result.score == pytest.approx(20.0)
    detector.reset()
    assert not detector.process(observation(0)).ready


def test_prefix_invariance_and_deterministic_scores() -> None:
    values = [observation(i, 10.0 if i != 10 else 15.0) for i in range(16)]
    factory = lambda: RollingMADStarter(DetectorConfig())  # noqa: E731
    short = [p for p, _ in process_stream(values[:12], factory)]
    long = [p for p, _ in process_stream(values, factory)]
    assert short == long[:12]


def test_series_isolation_and_cardinality_bound() -> None:
    data = [observation(0, 10, "a"), observation(0, 100, "b"), observation(1, 10, "a")]
    result = list(process_stream(data, lambda: RollingMADStarter(DetectorConfig())))
    assert result[-1][0].evidence.baseline == 10
    with pytest.raises(ContractError, match="Maximum active series"):
        list(process_stream(data, lambda: RollingMADStarter(DetectorConfig()), max_series=1))


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_observation_rejected(value: float) -> None:
    with pytest.raises(ContractError, match="finite"):
        observation(0, value)


def test_timestamp_offset_and_ordering() -> None:
    assert parse_timestamp("2026-01-01T05:30:00+05:30") == observation(0).timestamp
    with pytest.raises(ContractError, match="offset"):
        parse_timestamp("2026-01-01T00:00:00")
    detector = RollingMADStarter(DetectorConfig())
    detector.process(observation(0))
    with pytest.raises(ContractError, match="strictly increasing"):
        detector.process(observation(0))
    with pytest.raises(ContractError, match="one series"):
        detector.process(observation(1, series="other"))


def test_extreme_numeric_overflow_fails_explicitly() -> None:
    detector = RollingMADStarter(DetectorConfig(min_history=2))
    detector.process(observation(0, 1e308))
    detector.process(observation(1, 1e308))
    with pytest.raises(ContractError, match="overflow"):
        detector.process(observation(2, -1e308))


@pytest.mark.parametrize(
    "change",
    [
        {"window_size": 1},
        {"min_history": True},
        {"threshold": float("nan")},
        {"threshold": -1},
        {"scale_floor": 0},
        {"max_series": 0},
    ],
)
def test_invalid_config(change: dict[str, Any]) -> None:
    with pytest.raises(ContractError):
        DetectorConfig(**change)


def test_unknown_config_and_strict_csv(tmp_path: Path) -> None:
    config = tmp_path / "bad.json"
    config.write_text('{"typo": 3}', encoding="utf-8")
    with pytest.raises(ContractError, match="Unknown"):
        load_config(config)
    csv = tmp_path / "bad.csv"
    csv.write_text("series_id,timestamp,value,label\ns,2026-01-01T00:00:00Z,1,1\n")
    with pytest.raises(ContractError, match="header"):
        list(read_observations(csv))
    csv.write_text("series_id,timestamp,value\n")
    with pytest.raises(ContractError, match="no observations"):
        list(read_observations(csv))


def test_minimum_baseline_and_threshold_boundary() -> None:
    detector = RollingMADStarter(DetectorConfig(min_history=2, threshold=4, scale_floor=0.5))
    detector.process(observation(0))
    detector.process(observation(1))
    result = detector.process(observation(2, 12))
    assert result.score == 4
    assert result.label == "ANOMALOUS"


def test_event_matching_duplicate_episode_and_delay() -> None:
    records = [record(2), record(3, True), record(4, True), record(5), record(6, True), record(7)]
    result = event_metrics(records, [window(2, 6)])
    assert (result["tp"], result["fp"], result["fn"]) == (1, 1, 0)
    assert result["event_f1"] == pytest.approx(2 / 3)
    assert result["delay_seconds"] == [60]


def test_alert_starting_before_window_is_not_a_hit() -> None:
    result = event_metrics([record(2, True), record(3, True), record(4)], [window(3, 4)])
    assert (result["tp"], result["fp"], result["fn"]) == (0, 1, 1)


def test_event_boundaries_and_empty_truth_policy() -> None:
    result = event_metrics([record(2), record(3, True), record(4)], [window(3, 3)])
    assert result["event_f1"] == 1
    assert result["mean_delay_seconds"] == 0
    empty = event_metrics([record(2), record(3)], [])
    assert empty["event_f1"] == 0
    assert empty["mean_delay_seconds"] is None
    with pytest.raises(ContractError, match="empty"):
        event_metrics([], [])


def test_overlap_coverage_and_schema_validation() -> None:
    with pytest.raises(ContractError, match="Overlapping"):
        event_metrics([record(2), record(5)], [window(2, 4), window(4, 5)])
    with pytest.raises(ContractError, match="coverage"):
        event_metrics([record(2), record(3)], [window(2, 4)])
    broken = record(2)
    broken["label"] = "ANOMALOUS"
    with pytest.raises(ContractError, match="contradicts"):
        event_metrics([broken], [])


def test_synthetic_run_and_provenance(tmp_path: Path) -> None:
    destination = tmp_path / "run"
    result = run_file(
        FIXTURES / "synthetic_stream.csv",
        destination,
        DetectorConfig(),
        "synthetic_smoke",
        "synthetic-fixture-v1",
    )
    assert result["observations"] == 16
    assert result["anomalous_points"] == 1
    assert not result["official_submission_ready"]
    assert b"\r" not in (destination / "predictions.jsonl").read_bytes()
    metrics = evaluate_run(destination, FIXTURES / "synthetic_windows.json")
    assert metrics["evaluation_scope"] == "synthetic_smoke"
    assert not metrics["official_metric"]
    assert metrics["tp"] == 1
    assert metrics["fn"] == 0
    with pytest.raises(ContractError, match="already exists"):
        run_file(
            FIXTURES / "synthetic_stream.csv",
            destination,
            DetectorConfig(),
            "synthetic_smoke",
            "fixture",
        )
    predictions = destination / "predictions.jsonl"
    predictions.write_text(predictions.read_text() + "\n", encoding="utf-8")
    with pytest.raises(ContractError, match="checksum"):
        evaluate_run(destination, FIXTURES / "synthetic_windows.json")


def test_failed_run_leaves_no_partial_output(tmp_path: Path) -> None:
    csv = tmp_path / "bad.csv"
    csv.write_text(
        "series_id,timestamp,value\ns,2026-01-01T00:00:00Z,1\ns,2026-01-01T00:00:00Z,2\n"
    )
    with pytest.raises(ContractError):
        run_file(csv, tmp_path / "run", DetectorConfig(), "synthetic_smoke", "bad")
    assert not (tmp_path / "run").exists()
    assert not list(tmp_path.glob(".sentinel-*"))


def test_cli_errors_and_help(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        main(
            [
                "run",
                "--input",
                str(tmp_path / "missing.csv"),
                "--config",
                "configs/starter.json",
                "--output-dir",
                str(tmp_path / "run"),
                "--dataset-id",
                "missing",
                "--scope",
                "synthetic_smoke",
            ]
        )
        == 2
    )
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    assert "unofficial" in capsys.readouterr().out


def test_scores_ignore_elapsed_time() -> None:
    prediction = RollingMADStarter(DetectorConfig()).process(observation(0))
    first = prediction_record(prediction, 1)
    second = prediction_record(replace(prediction), 999)
    assert {k: v for k, v in first.items() if k != "elapsed_ns"} == {
        k: v for k, v in second.items() if k != "elapsed_ns"
    }
    json.dumps(first, allow_nan=False)
