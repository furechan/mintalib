# Backlog

Items decided or considered but not scheduled. Add new items at the end.

## Indicators

- ~~Adopt the barcalc/bearta regression naming scheme and diagnostics~~ — done in 0.1.0 (2026-07-11): family-prefixed rename (`LINREG`, `LINREG_SLOPE`, `LINREG_RVALUE`, `QUADREG`, `QUADREG_CURVE`) as a clean break without deprecation aliases, plus the missing diagnostics (`LINREG_RMSE`, `QUADREG_SLOPE`, `QUADREG_RVALUE`, `QUADREG_RMSE`). Deviation from barcalc: `QUADREG_SLOPE` returns the slope at the current bar (not the window midpoint) and takes an `offset` parameter.
- Review BBANDS-family price source: `calc_bbands`/`calc_bbp`/`calc_bbw` (cython/bbands.pxi) all use `calc_typprice`; standard Bollinger (and talib) uses close — mplchart switched to close in 2026-07. Decide close vs typ (or an explicit price-source parameter).

