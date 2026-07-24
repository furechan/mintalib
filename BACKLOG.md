# Backlog

Items decided or considered but not scheduled. Add new items at the end.

## Indicators

- ~~Adopt the barcalc/bearta regression naming scheme and diagnostics~~ — done in 0.1.0 (2026-07-11): family-prefixed rename (`LINREG`, `LINREG_SLOPE`, `LINREG_RVALUE`, `QUADREG`, `QUADREG_CURVE`) as a clean break without deprecation aliases, plus the missing diagnostics (`LINREG_RMSE`, `QUADREG_SLOPE`, `QUADREG_RVALUE`, `QUADREG_RMSE`). Deviation from barcalc: `QUADREG_SLOPE` returns the slope at the current bar (not the window midpoint) and takes an `offset` parameter.
- ~~Review BBANDS-family price source~~ — done in 0.1.2 (2026-07-24): BBANDS/BBP/BBW became series indicators defaulting to close (matches talib, covered by parity tests); old behavior via `TYPPRICE() | BBANDS(20)` or `src=TYPPRICE()`.
- ~~Rename MIDPRICE into MEDPRICE (established convention)~~ — done in 0.1.2 (2026-07-24): `calc_midprice` → `calc_medprice`, `MIDPRICE` → `MEDPRICE` across all interfaces; `PRICE` item `'mid'` → `'med'` (`'hl2'` unchanged).

