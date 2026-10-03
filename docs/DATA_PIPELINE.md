# Data pipeline

## Contract

Collectors convert source-specific data into normalized observations. Source adapters are deliberately separate from model code.

Each observation records:

- source identity
- event/kickoff time
- observation/publication time
- retrieval time where relevant
- team/player identifiers
- raw values and normalized values

The model may only consume a value when its observation time precedes the forecast cutoff.

## Initial normalized match fields

`match_id,kickoff_at,observed_at,team_a,team_b,goals_a,goals_b,competition,neutral`

Future adapters should add separate timestamped tables for:

- rankings / Elo
- xG and shot quality
- squads, injuries and suspensions
- player minutes and workload
- venue/travel/rest
- managers and tactical regime changes

Do not overwrite historical observations when a source revises a value. Append a new version with a later `observed_at`.

## Source policy

Prefer official competition/federation data for fixtures, results, squads and disciplinary status. Statistical providers can supply richer event/xG data when licensing permits. Every adapter must retain provenance and timestamps.

## Update cycle

1. ingest new observations
2. validate schemas and timestamps
3. build features at historical cutoffs
4. run walk-forward folds
5. fit challenger parameters only on past data
6. compare challenger with champion on unseen windows
7. promote only if policy passes
8. snapshot forecasts and metrics
