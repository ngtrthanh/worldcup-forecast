from datetime import datetime, timezone

from worldcup_forecast.data import MatchRecord, available_before
from worldcup_forecast.features import rolling_features
from worldcup_forecast.simulation import simulate_knockout


UTC=timezone.utc


def test_cutoff_blocks_future_information():
    old=MatchRecord("1",datetime(2026,1,1,tzinfo=UTC),datetime(2025,12,31,tzinfo=UTC),"A","B",1,0)
    future=MatchRecord("2",datetime(2026,3,1,tzinfo=UTC),datetime(2026,2,28,tzinfo=UTC),"A","B",9,0)
    cutoff=datetime(2026,2,1,tzinfo=UTC)
    assert available_before([old,future],cutoff)==[old]
    assert rolling_features([old,future],"A",cutoff).games==1


def test_simulation_probabilities_sum_to_one():
    probs=simulate_knockout(["A","B","C","D"],lambda a,b:0.5,iterations=1000,seed=7)
    assert abs(sum(probs.values())-1.0)<1e-12
