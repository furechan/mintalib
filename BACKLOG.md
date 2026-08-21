# Backlog

Items decided or considered but not scheduled. Add new items at the end.

## Indicators

- ~~Adopt the barcalc/bearta regression naming scheme and diagnostics~~ — done in 0.1.0 (2026-07-11): family-prefixed rename (`LINREG`, `LINREG_SLOPE`, `LINREG_RVALUE`, `QUADREG`, `QUADREG_CURVE`) as a clean break without deprecation aliases, plus the missing diagnostics (`LINREG_RMSE`, `QUADREG_SLOPE`, `QUADREG_RVALUE`, `QUADREG_RMSE`). Deviation from barcalc: `QUADREG_SLOPE` returns the slope at the current bar (not the window midpoint) and takes an `offset` parameter.
- ~~Review BBANDS-family price source~~ — done in 0.1.2 (2026-07-24): BBANDS/BBP/BBW became series indicators defaulting to close (matches talib, covered by parity tests); old behavior via `TYPPRICE() | BBANDS(20)` or `src=TYPPRICE()`.
- ~~Rename MIDPRICE into MEDPRICE (established convention)~~ — done in 0.1.2 (2026-07-24): `calc_midprice` → `calc_medprice`, `MIDPRICE` → `MEDPRICE` across all interfaces; `PRICE` item `'mid'` → `'med'` (`'hl2'` unchanged).
- Fix the off-by-one in `calc_ker` (`src/mintalib/cython/kama.pxi`): the numerator spans `period - 1` changes while the denominator spans `period`, so the efficiency ratio reads systematically low and `calc_kama` is correspondingly slower than Kaufman's. The tell is a monotone ramp, which is perfectly efficient by definition and must score exactly 1.0 — `KER(3)` returns 0.833 on it, drifting further down as the period grows. Cause looks like the priming pass of the `while ercnt >= period` loop: on the first full window `py` is still `NAN`, so that pass sets a correct `erval` but does not decrement `ercnt`, and the next pass overwrites it with a numerator one change short; the window bookkeeping stays offset from then on. Raised 2026-08-21 from bartons, which implemented its own KER/KAMA kernel, cross-checked against mintalib on clean data and found `max_abs_diff` 0.41 on KER; reproducing the exact span mismatch (numerator over 9 changes, denominator over 10, at `period=10`) matched mintalib to zero difference, so it is a precise off-by-one rather than a convention difference. bearta is unaffected — its `direction` telescopes over the same `period` changes as its `volatility`. Note bartons deliberately does not match these numbers, so fixing this converges the two.


## Publishing

- ~~Add PyPI project urls to pyproject~~ — done 2026-07-25: added `urls.documentation`, `urls.repository`, `urls.changelog` matching mplchart's format; takes effect when 0.1.3 publishes
- ~~Register https://furechan.github.io/mintalib/ on Google Search Console~~ — done 2026-07-25: URL-prefix property verified via the account-level HTML file reused from mplchart (injected at CI time in pages.yml, deploys at site root), sitemap.xml submitted


## Typing

- Swap the `ExprFactory` overload order in `model/expression.py` so the canonical params-first form is declared first. Editors list overloads in declaration order, so the expression-first shim (`(src: pl.Expr, /, *args, **kwargs)`) is what currently shows first in the signature dropdown, ahead of the real signature. Raised 2026-08-13 from bearta, which ported this protocol to make `expr.pipe(SMA, 20)` type-check and hit the dropdown noise immediately; both orders were verified equivalent there under ty and pyright (`Expr.pipe` still accepts the factories, chaining still resolves), so the change is display-only. Confirm mintalib's factories are params-first in the same way before swapping — canonical-first only makes sense if the expression-first overload is the compatibility shim rather than the primary form.
