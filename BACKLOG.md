# Backlog

Items decided or considered but not scheduled. Add new items at the end.

## Indicators

- RSI null handling is inconsistent with EMA: EMA skips a null (carrying the average across the gap), but RSI re-seeds `prev` on a null, breaking the delta chain so the price move across the gap is not measured. Update RSI to keep `prev` across nulls (bridge) so it is consistent with the EMA/RMA skip behavior. Surfaced by bartons, which deliberately chose bridge for this reason (see bartons CHANGELOG 0.1.0).
- Adopt the regression naming scheme settled in barcalc/bearta (python-dev, 2026-07-03): bare `LINREG(period, offset)` is the regression-line overlay (least squares moving average — == TA-Lib `LINEARREG`, `offset=1` == `TSF`; matches TradingView `ta.linreg`), diagnostics are family-prefixed (`LINREG_SLOPE`, `LINREG_RVALUE`, `LINREG_RMSE`), and a `QUADREG` family mirrors it (`QUADREG`, `QUADREG_CURVE`, ...). Would retire/deprecate the flat `SLOPE`, `RVALUE`, `ERROR`, `TSF`, `CURVE` — breaking rename for a published package, so needs deprecation aliases and a major-ish version bump.

