# Backlog

Items decided or considered but not scheduled. Add new items at the end.

## CI

- Remove ruff from GitHub workflow (python-package.yaml) — lint locally only

## API

- Deprecate `@` operator for indicator composition — emit `DeprecationWarning` when `indicator @ indicator` is used
- Promote `|` as the canonical chaining operator (`ROC(1) | EMA(20)` instead of `EMA(20) @ ROC(1)`)
- Update all docs and examples to use `|` instead of `@`

## Correctness

- Fix CCI to use true MAD (mean of |x - mean(x)| over the same window) — current implementation subtracts each element's own rolling mean, which diverges from TA-Lib's correct calculation
