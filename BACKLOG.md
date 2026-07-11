# Backlog

Items decided or considered but not scheduled. Add new items at the end.

## Indicators

- Adopt the regression naming scheme settled in barcalc/bearta (python-dev, 2026-07-03): bare `LINREG(period, offset)` is the regression-line overlay (least squares moving average — == TA-Lib `LINEARREG`, `offset=1` == `TSF`; matches TradingView `ta.linreg`), diagnostics are family-prefixed (`LINREG_SLOPE`, `LINREG_RVALUE`, `LINREG_RMSE`), and a `QUADREG` family mirrors it (`QUADREG`, `QUADREG_CURVE`, ...). Would retire/deprecate the flat `SLOPE`, `RVALUE`, `ERROR`, `TSF`, `CURVE` — breaking rename for a published package, so needs deprecation aliases and a major-ish version bump.

