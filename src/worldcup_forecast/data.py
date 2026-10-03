from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return dt.astimezone(timezone.utc)


@dataclass(frozen=True)
class MatchRecord:
    match_id: str
    kickoff_at: datetime
    observed_at: datetime
    team_a: str
    team_b: str
    goals_a: int
    goals_b: int
    competition: str = ""
    neutral: bool = True

    def __post_init__(self) -> None:
        if self.observed_at > self.kickoff_at:
            raise ValueError("match observation cannot be later than kickoff")


REQUIRED = {"match_id","kickoff_at","observed_at","team_a","team_b","goals_a","goals_b"}


def load_matches_csv(path: str | Path) -> list[MatchRecord]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        reader=csv.DictReader(f)
        missing=REQUIRED-set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")
        rows=[]
        for r in reader:
            rows.append(MatchRecord(
                match_id=r["match_id"],
                kickoff_at=parse_time(r["kickoff_at"]),
                observed_at=parse_time(r["observed_at"]),
                team_a=r["team_a"],
                team_b=r["team_b"],
                goals_a=int(r["goals_a"]),
                goals_b=int(r["goals_b"]),
                competition=r.get("competition",""),
                neutral=r.get("neutral","true").lower() in {"1","true","yes"},
            ))
    return sorted(rows,key=lambda x:x.kickoff_at)


def available_before(records: Iterable[MatchRecord], cutoff: datetime) -> list[MatchRecord]:
    cutoff=cutoff.astimezone(timezone.utc)
    return [r for r in records if r.observed_at < cutoff and r.kickoff_at < cutoff]
