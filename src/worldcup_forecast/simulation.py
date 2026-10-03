from __future__ import annotations

import random
from collections import Counter
from typing import Callable, Hashable, Sequence


def simulate_knockout(
    teams: Sequence[Hashable],
    probability: Callable[[Hashable,Hashable],float],
    iterations: int=10000,
    seed: int=1,
) -> dict[Hashable,float]:
    if not teams or len(teams) & (len(teams)-1):
        raise ValueError("team count must be a non-zero power of two")
    rng=random.Random(seed)
    titles=Counter()
    for _ in range(iterations):
        field=list(teams)
        while len(field)>1:
            nxt=[]
            for a,b in zip(field[0::2],field[1::2]):
                nxt.append(a if rng.random()<probability(a,b) else b)
            field=nxt
        titles[field[0]]+=1
    return {t:titles[t]/iterations for t in teams}
