# Backlog

Items decided or considered but not scheduled. Add new items at the end.

## Indicators

- ~~Adopt the barcalc/bearta regression naming scheme and diagnostics~~ — done in 0.1.0 (2026-07-11): family-prefixed rename (`LINREG`, `LINREG_SLOPE`, `LINREG_RVALUE`, `QUADREG`, `QUADREG_CURVE`) as a clean break without deprecation aliases, plus the missing diagnostics (`LINREG_RMSE`, `QUADREG_SLOPE`, `QUADREG_RVALUE`, `QUADREG_RMSE`). Deviation from barcalc: `QUADREG_SLOPE` returns the slope at the current bar (not the window midpoint) and takes an `offset` parameter.
- ~~Review BBANDS-family price source~~ — done in 0.1.2 (2026-07-24): BBANDS/BBP/BBW became series indicators defaulting to close (matches talib, covered by parity tests); old behavior via `TYPPRICE() | BBANDS(20)` or `src=TYPPRICE()`.
- ~~Rename MIDPRICE into MEDPRICE (established convention)~~ — done in 0.1.2 (2026-07-24): `calc_midprice` → `calc_medprice`, `MIDPRICE` → `MEDPRICE` across all interfaces; `PRICE` item `'mid'` → `'med'` (`'hl2'` unchanged).


## Publishing

- ~~Add PyPI project urls to pyproject~~ — done 2026-07-25: added `urls.documentation`, `urls.repository`, `urls.changelog` matching mplchart's format; takes effect when 0.1.3 publishes
- Register https://furechan.github.io/mintalib/ on Google Search Console — URL-prefix property, HTML verification file into docs source so it deploys at site root, submit sitemap.xml, request indexing on key pages (same flow as mplchart, 2026-07-25)
