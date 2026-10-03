# WorldCup Forecast

A reproducible, continuously updated forecasting system for men's international football and FIFA World Cup outcomes.

## Goals

- Produce calibrated match-advancement and tournament-winning probabilities.
- Update team strength as new evidence arrives without leaking future information.
- Evaluate with walk-forward backtests, Brier score, log loss, calibration, and upset diagnostics.
- Preserve every forecast snapshot so later audits distinguish genuine forecasting skill from hindsight.

## Current model

```
R(team,t) = 0.45*E + 0.20*F + 0.15*D + 0.10*X + 0.05*A + 0.05*C
```

Where:

- **E**: long-run Elo/FIFA-style strength prior
- **F**: exponentially weighted recent and tournament form
- **D**: defensive suppression
- **X**: xG / chance-quality differential
- **A**: squad availability and depth
- **C**: context: rest, travel, venue, host effect

The production design uses a slow-moving prior plus a faster state model. Knockout matches explicitly model 90 minutes, extra time, and penalties.

## Learning loop

```
collect -> timestamp -> validate -> build features -> walk-forward backtest
        -> optimize challenger -> calibrate -> accept/reject -> simulate
        -> snapshot/version -> repeat
```

A challenger only replaces production when it improves genuinely unseen periods and does not materially worsen calibration.

## Repository layout

- `config/model.yaml` — production coefficients and learning rules
- `src/worldcup_forecast/model.py` — core probability model
- `src/worldcup_forecast/evaluation.py` — Brier/log-loss/calibration metrics
- `src/worldcup_forecast/update_loop.py` — champion/challenger update logic
- `schemas/match_snapshot.schema.json` — immutable pre-kickoff record format
- `docs/MODEL.md` — methodology and anti-leakage rules
- `docs/VALIDATION.md` — walk-forward validation protocol
- `data/baselines/2030-2026-10-03.json` — frozen early 2030 baseline

## Frozen baseline — 2026-10-03

The early 2030 tournament forecast discussed when this repository was initialized is preserved as a baseline rather than silently rewritten by future model versions.

| Team | Title probability |
|---|---:|
| Spain | 0.18 |
| France | 0.14 |
| Argentina | 0.13 |
| England | 0.12 |
| Brazil | 0.10 |
| Portugal | 0.07 |
| Morocco | 0.05 |
| Norway | 0.04 |
| Other teams | 0.17 |

These are model estimates, not official FIFA probabilities.

## Principles

1. No future data in historical forecasts.
2. Every input must carry an `observed_at` timestamp.
3. Never tune on the same matches used for final evaluation.
4. Prefer probability calibration over raw pick accuracy.
5. Penalty shootouts are a separate stochastic phase.
6. Surprising results do not automatically imply bad forecasts.
7. All production changes must be versioned and reproducible.

## Quick start

```bash
python -m pip install -e .
python -m worldcup_forecast.model
```

This repository starts with a transparent baseline implementation. Data collectors and richer models can be added without changing the audit contract.
