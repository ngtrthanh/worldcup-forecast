from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import exp
from typing import Iterable

from .data import MatchRecord, available_before


@dataclass(frozen=True)
class RollingFeatures:
    games: int
    points_per_game: float
    goal_diff_per_game: float
    goals_against_per_game: float


def team_history(records: Iterable[MatchRecord], team: str, cutoff: datetime) -> list[MatchRecord]:
    return [m for m in available_before(records, cutoff) if team in (m.team_a,m.team_b)]


def rolling_features(records: Iterable[MatchRecord], team: str, cutoff: datetime, half_life_games: float=5.0) -> RollingFeatures:
    history=team_history(records,team,cutoff)
    if not history:
        return RollingFeatures(0,0.0,0.0,0.0)
    weighted=[]
    n=len(history)
    for idx,m in enumerate(history):
        age=n-1-idx
        w=exp(-0.6931471805599453*age/half_life_games)
        gf,ga=(m.goals_a,m.goals_b) if m.team_a==team else (m.goals_b,m.goals_a)
        pts=3 if gf>ga else 1 if gf==ga else 0
        weighted.append((w,pts,gf-ga,ga))
    sw=sum(x[0] for x in weighted)
    return RollingFeatures(
        games=n,
        points_per_game=sum(w*p for w,p,_,__ in weighted)/sw,
        goal_diff_per_game=sum(w*gd for w,_,gd,__ in weighted)/sw,
        goals_against_per_game=sum(w*ga for w,_,__,ga in weighted)/sw,
    )
