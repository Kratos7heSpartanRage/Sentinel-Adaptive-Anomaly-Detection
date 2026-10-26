"""Version 1 shared contracts. Coordinate breaking changes with Ayush."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from math import isfinite
from typing import Literal, Protocol

SCHEMA_VERSION = "1.0"
Label = Literal["NORMAL", "ANOMALOUS"]
EvaluationScope = Literal["synthetic_smoke", "development_validation"]


class ContractError(ValueError):
    """Invalid data, configuration, or serialized contract."""


def parse_timestamp(value: str) -> datetime:
    if not isinstance(value, str):
        raise ContractError("Timestamp must be an ISO string")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"Invalid ISO timestamp: {value!r}") from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise ContractError("Timestamp requires an explicit UTC offset; do not guess NAB timezone")
    return result.astimezone(UTC)


def timestamp_text(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class Observation:
    series_id: str
    timestamp: datetime
    value: float

    def __post_init__(self) -> None:
        if not isinstance(self.series_id, str) or not self.series_id.strip():
            raise ContractError("series_id must be nonempty")
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ContractError("Observation timestamp must be timezone aware")
        if type(self.value) not in (int, float) or not isfinite(self.value):
            raise ContractError("Observation value must be finite")


@dataclass(frozen=True)
class Evidence:
    baseline: float | None
    scale: float | None
    residual: float | None
    history_size: int
    reason: str
    component_scores: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class Prediction:
    series_id: str
    timestamp: datetime
    value: float
    score: float | None
    threshold: float
    label: Label
    ready: bool
    evidence: Evidence


@dataclass(frozen=True)
class AnomalyWindow:
    series_id: str
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.series_id, str) or not self.series_id.strip():
            raise ContractError("Window series_id must be nonempty")
        if self.start.tzinfo is None or self.end.tzinfo is None:
            raise ContractError("Window timestamps must be timezone aware")
        if self.end < self.start:
            raise ContractError("Window end precedes start")


@dataclass(frozen=True)
class FeatureFrame:
    """Future residual detector input; expected statistics use prior observations only."""

    series_id: str
    timestamp: datetime
    expected_level: float | None
    expected_delta: float | None
    scale: float | None
    delta: float | None
    seasonal_expected: float | None
    history_size: int
    ready: bool


class FeatureExtractor(Protocol):
    """One series; construct frame before incorporating the current value into statistics."""

    def process(self, observation: Observation) -> FeatureFrame: ...

    def reset(self) -> None: ...


class Detector(Protocol):
    """One instance per series. Score before updating; never accept labels."""

    def process(self, observation: Observation) -> Prediction: ...

    def reset(self) -> None: ...
