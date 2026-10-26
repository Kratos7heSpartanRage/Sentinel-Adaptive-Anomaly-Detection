from collections import deque
from math import isfinite
from statistics import median

from sentinel.config import DetectorConfig
from sentinel.contracts import ContractError, Evidence, Observation, Prediction


class RollingMADStarter:
    """Minimal causal baseline. Includes anomalies in updates; no drift guard yet.

    The score is a robust standardized deviation, not an anomaly probability.
    Median/MAD are recomputed: O(W log W) time and O(W) memory per observation.
    """

    def __init__(self, config: DetectorConfig) -> None:
        self.config = config
        self.reset()

    def reset(self) -> None:
        self._history: deque[float] = deque(maxlen=self.config.window_size)
        self._last: Observation | None = None

    def process(self, observation: Observation) -> Prediction:
        if self._last is not None:
            if observation.series_id != self._last.series_id:
                raise ContractError("A detector instance handles only one series")
            if observation.timestamp <= self._last.timestamp:
                raise ContractError("Timestamps must be strictly increasing within each series")
        history_size = len(self._history)
        baseline = median(self._history) if self._history else None
        ready = history_size >= self.config.min_history
        score = scale = residual = None
        if ready:
            assert baseline is not None
            mad = median(abs(value - baseline) for value in self._history)
            scale = max(1.4826 * mad, self.config.scale_floor)
            residual = observation.value - baseline
            score = abs(residual) / scale
            if not all(isfinite(value) for value in (baseline, scale, residual, score)):
                raise ContractError(
                    "Numerical overflow in baseline calculation; rescale input explicitly"
                )
        anomalous = score is not None and score >= self.config.threshold
        prediction = Prediction(
            series_id=observation.series_id,
            timestamp=observation.timestamp,
            value=observation.value,
            score=score,
            threshold=self.config.threshold,
            label="ANOMALOUS" if anomalous else "NORMAL",
            ready=ready,
            evidence=Evidence(
                baseline=baseline,
                scale=scale,
                residual=residual,
                history_size=history_size,
                reason="warmup" if not ready else "rolling_mad_deviation",
                component_scores={} if score is None else {"level": score},
            ),
        )
        self._history.append(observation.value)
        self._last = observation
        return prediction
