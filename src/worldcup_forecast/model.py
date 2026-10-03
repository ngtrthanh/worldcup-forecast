from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Mapping


@dataclass(frozen=True)
class Weights:
    strength_prior: float = 0.45
    recent_form: float = 0.20
    defense: float = 0.15
    xg_quality: float = 0.10
    availability_depth: float = 0.05
    context: float = 0.05

    def validate(self) -> None:
        total = sum(self.__dict__.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"weights must sum to 1.0, got {total:.6f}")


@dataclass(frozen=True)
class TeamFeatures:
    strength_prior: float
    recent_form: float
    defense: float
    xg_quality: float
    availability_depth: float
    context: float


class ForecastModel:
    """Transparent baseline model.

    Feature values should be normalized onto a common scale before use.
    All features must be computed from observations available before kickoff.
    """

    def __init__(self, weights: Weights | None = None, logistic_scale: float = 1.0):
        self.weights = weights or Weights()
        self.weights.validate()
        self.logistic_scale = logistic_scale

    def rating(self, f: TeamFeatures) -> float:
        w = self.weights
        return (
            w.strength_prior * f.strength_prior
            + w.recent_form * f.recent_form
            + w.defense * f.defense
            + w.xg_quality * f.xg_quality
            + w.availability_depth * f.availability_depth
            + w.context * f.context
        )

    def advance_probability(
        self,
        team_a: TeamFeatures,
        team_b: TeamFeatures,
        *,
        floor: float = 0.02,
        ceiling: float = 0.98,
    ) -> float:
        delta = self.rating(team_a) - self.rating(team_b)
        p = 1.0 / (1.0 + exp(-self.logistic_scale * delta))
        return min(ceiling, max(floor, p))

    @staticmethod
    def update_prior(base: float, tournament_state: float, lam: float) -> float:
        if not 0.0 <= lam <= 1.0:
            raise ValueError("lambda must be between 0 and 1")
        return (1.0 - lam) * base + lam * tournament_state


if __name__ == "__main__":
    model = ForecastModel()
    equal = TeamFeatures(0, 0, 0, 0, 0, 0)
    print(f"Equal teams: {model.advance_probability(equal, equal):.3f}")
