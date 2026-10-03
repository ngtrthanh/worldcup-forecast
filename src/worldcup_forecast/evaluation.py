from __future__ import annotations

from dataclasses import dataclass
from math import log
from typing import Iterable


EPS = 1e-15


def brier_score(probabilities: Iterable[float], outcomes: Iterable[int]) -> float:
    pairs = list(zip(probabilities, outcomes))
    if not pairs:
        raise ValueError("no predictions")
    return sum((p - y) ** 2 for p, y in pairs) / len(pairs)


def log_loss(probabilities: Iterable[float], outcomes: Iterable[int]) -> float:
    pairs = list(zip(probabilities, outcomes))
    if not pairs:
        raise ValueError("no predictions")
    total = 0.0
    for p, y in pairs:
        p = min(1.0 - EPS, max(EPS, p))
        total -= y * log(p) + (1 - y) * log(1 - p)
    return total / len(pairs)


@dataclass(frozen=True)
class CalibrationBin:
    lower: float
    upper: float
    count: int
    mean_probability: float
    observed_rate: float


def calibration_table(
    probabilities: Iterable[float],
    outcomes: Iterable[int],
    bins: int = 10,
) -> list[CalibrationBin]:
    pairs = list(zip(probabilities, outcomes))
    result: list[CalibrationBin] = []
    for i in range(bins):
        lo = i / bins
        hi = (i + 1) / bins
        chunk = [
            (p, y)
            for p, y in pairs
            if (lo <= p < hi) or (i == bins - 1 and p == 1.0)
        ]
        if not chunk:
            continue
        result.append(
            CalibrationBin(
                lower=lo,
                upper=hi,
                count=len(chunk),
                mean_probability=sum(p for p, _ in chunk) / len(chunk),
                observed_rate=sum(y for _, y in chunk) / len(chunk),
            )
        )
    return result
