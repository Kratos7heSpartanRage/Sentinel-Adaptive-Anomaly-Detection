import json
from dataclasses import asdict, dataclass
from math import isfinite
from pathlib import Path
from typing import Any

from sentinel.contracts import ContractError


@dataclass(frozen=True)
class DetectorConfig:
    window_size: int = 32
    min_history: int = 8
    threshold: float = 4.0
    scale_floor: float = 0.1
    max_series: int = 100

    def __post_init__(self) -> None:
        for name in ("window_size", "min_history", "max_series"):
            if type(getattr(self, name)) is not int:
                raise ContractError(f"{name} must be an integer")
        if not 2 <= self.min_history <= self.window_size:
            raise ContractError("Require 2 <= min_history <= window_size")
        if self.max_series < 1:
            raise ContractError("max_series must be positive")
        for name in ("threshold", "scale_floor"):
            value = getattr(self, name)
            if type(value) not in (int, float) or not isfinite(value) or value <= 0:
                raise ContractError(f"{name} must be finite and positive")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_config(path: Path) -> DetectorConfig:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ContractError("Config must be a JSON object")
    unknown = set(payload) - set(DetectorConfig.__dataclass_fields__)
    if unknown:
        raise ContractError(f"Unknown config keys: {sorted(unknown)}")
    return DetectorConfig(**payload)
