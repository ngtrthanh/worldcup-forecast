from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log
from typing import Callable, Sequence


@dataclass(frozen=True)
class Candidate:
    form_weight: float
    defense_weight: float
    scale: float


@dataclass(frozen=True)
class CandidateScore:
    candidate: Candidate
    log_loss: float
    count: int


def binary_log_loss(p: float, y: int) -> float:
    p=min(1-1e-12,max(1e-12,p))
    return -(y*log(p)+(1-y)*log(1-p))


def grid_candidates() -> list[Candidate]:
    return [Candidate(f,d,s) for f,d,s in product(
        (0.10,0.15,0.20,0.25),
        (0.10,0.15,0.20),
        (0.5,0.75,1.0,1.25,1.5),
    ) if f+d < 0.60]


def choose_challenger(
    examples: Sequence[object],
    predict: Callable[[object,Candidate],float],
    outcome: Callable[[object],int],
    candidates: Sequence[Candidate] | None=None,
) -> CandidateScore:
    if not examples:
        raise ValueError("no validation examples")
    best=None
    for c in candidates or grid_candidates():
        losses=[binary_log_loss(predict(e,c),outcome(e)) for e in examples]
        score=CandidateScore(c,sum(losses)/len(losses),len(losses))
        if best is None or score.log_loss < best.log_loss:
            best=score
    assert best is not None
    return best
