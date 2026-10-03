from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Sequence


@dataclass(frozen=True)
class Fold:
    train_end: datetime
    validation_end: datetime


@dataclass(frozen=True)
class Prediction:
    match_id: str
    kickoff_at: datetime
    probability: float
    outcome: int


def walk_forward(
    matches: Sequence[object],
    folds: Sequence[Fold],
    fit: Callable[[list[object]],object],
    predict: Callable[[object,object],float],
    kickoff: Callable[[object],datetime],
    match_id: Callable[[object],str],
    outcome: Callable[[object],int],
) -> list[Prediction]:
    predictions=[]
    for fold in folds:
        train=[m for m in matches if kickoff(m) < fold.train_end]
        valid=[m for m in matches if fold.train_end <= kickoff(m) < fold.validation_end]
        if not train or not valid:
            continue
        model=fit(train)
        for m in valid:
            predictions.append(Prediction(
                match_id=match_id(m),
                kickoff_at=kickoff(m),
                probability=predict(model,m),
                outcome=outcome(m),
            ))
    return predictions
