# Model methodology

## Purpose

WorldCup Forecast estimates probabilities, not certainties. A correct 55% prediction that loses is not automatically a bad forecast; a confidently wrong 95% prediction is much more informative.

## Production architecture

### 1. Slow prior

Long-run team strength is anchored by an Elo/FIFA-style prior. This avoids overreacting to small tournament samples.

### 2. Fast state

Recent evidence updates the prior through:

- opponent-adjusted competitive form
- expected-goal and chance-quality differential
- defensive suppression
- squad availability and depth
- player minutes / workload when available
- rest and travel
- venue and host effects
- manager/system changes where objectively encoded

### 3. Match layer

Convert rating difference to win/advance probability. A richer implementation should estimate score distributions with Poisson or related count models.

### 4. Knockout layer

Model 90 minutes, extra time and penalties separately. Shootouts should generally shrink toward 50/50 unless reliable keeper/taker evidence exists.

### 5. Tournament simulator

Run Monte Carlo simulations using the match probabilities to estimate round-reach and title probabilities.

## Dynamic strength update

The baseline uses:

```
E_t = (1 - lambda_t) * E_0 + lambda_t * T_t
```

The tournament contribution rises by stage but remains constrained so one result cannot erase the prior.

## Anti-leakage contract

Every source datum must have an observation timestamp. When reconstructing a forecast for match M, no feature may use information observed after the forecast cutoff.

Examples of prohibited leakage:

- later rankings
- final tournament statistics
- injuries reported after kickoff
- a player's minutes in future matches
- later xG revisions unavailable at forecast time
- coefficients selected because they improve the same held-out tournament being reported

## Optimization

Primary metric: log loss.

Secondary diagnostics:

- Brier score
- expected calibration error
- calibration slope/intercept
- sharpness
- pick accuracy (diagnostic only)
- performance by probability band
- performance by competition/stage
- favorite/underdog asymmetry

## Champion/challenger rule

A new parameter set must beat the production champion on genuinely later validation data and stay within the allowed calibration-regression bound. Otherwise production is unchanged.
