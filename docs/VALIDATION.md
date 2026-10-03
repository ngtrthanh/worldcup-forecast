# Walk-forward validation

## Required ordering

Sort matches by kickoff time. Training data must always precede validation data.

A typical fold:

1. train through date T
2. calibrate using data available through T
3. freeze parameters
4. predict the next international window or tournament block
5. reveal outcomes
6. score predictions
7. advance T and repeat

## Never use random train/test splits

Random splitting leaks future team quality, manager changes, player development and competition information backward in time.

## Promotion metrics

At minimum record:

- mean log loss
- Brier score
- calibration error
- prediction count
- confidence-band reliability

Also retain individual match snapshots so aggregate metrics can always be reproduced.

## Parameter optimization

Prefer constrained optimization and regularization. Candidate weights should:

- sum to 1
- remain nonnegative for the baseline linear ensemble
- be chosen only on training/history
- be evaluated on later windows

More flexible learners may be added as challengers, but the transparent baseline remains useful as a control.

## 2026 audit

The 2026 World Cup knockout stage is a valuable validation block, especially:

- Germany vs Paraguay
- Netherlands vs Morocco
- Brazil vs Norway
- penalty-decided matches
- elite late-stage matches among Spain, France, Argentina and England

Do not tune a final production model directly on these outcomes and then report its score on the same games as out-of-sample performance.
