from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    log_loss: float
    brier: float
    calibration_error: float


@dataclass(frozen=True)
class PromotionPolicy:
    max_calibration_regression: float = 0.01
    min_log_loss_improvement: float = 0.0


def should_promote(
    champion: Metrics,
    challenger: Metrics,
    policy: PromotionPolicy = PromotionPolicy(),
) -> bool:
    log_loss_gain = champion.log_loss - challenger.log_loss
    calibration_regression = (
        challenger.calibration_error - champion.calibration_error
    )
    return (
        log_loss_gain > policy.min_log_loss_improvement
        and calibration_regression <= policy.max_calibration_regression
    )
