# Change Log

## 0.1.0
- Added the regression diagnostics missing vs barcalc/bearta: `LINREG_RMSE`, `QUADREG_SLOPE`, `QUADREG_RVALUE`, `QUADREG_RMSE` (core functions `calc_linreg_rmse`, `calc_quadreg_slope`, `calc_quadreg_rvalue`, `calc_quadreg_rmse`). `QUADREG_SLOPE` deviates from barcalc on purpose: it returns the slope of the regression parabola at the current bar (barcalc evaluates it at the window midpoint) and accepts an `offset` parameter to project the slope forward, like `QUADREG`. `QUADREG_RVALUE` is the partial correlation of the quadratic term given the linear term, and the RMSE statistics are the residual RMSE of the full fit — both match barcalc's definitions. New `tests/test_regression.py` verifies every LINREG/QUADREG statistic against explicit per-window `numpy.polyfit` references
- Breaking: renamed the regression indicators to the family-prefixed naming scheme used in barcalc/bearta: `TSF` → `LINREG` (value of the regression line at the current bar — matches TA-Lib `LINEARREG`; `offset=1` matches TA-Lib `TSF`), `SLOPE` → `LINREG_SLOPE`, `RVALUE` → `LINREG_RVALUE`, `QSF` → `QUADREG`, `CURVE` → `QUADREG_CURVE`. Core functions renamed accordingly (`calc_linreg`, `calc_linreg_slope`, `calc_linreg_rvalue`, `calc_quadreg`, `calc_quadreg_curve`) and Cython sources renamed `slope.pxi` → `linreg.pxi`, `curve.pxi` → `quadreg.pxi`. Clean break — the old flat names are removed without deprecation aliases, hence the minor version bump (this release supersedes the unreleased 0.0.37)
- Renamed `meta/` to `notes/` for internal notes and moved `paramspec-proposal.md` out of `docs/`, which now contains only generated user-facing API docs
- Docs now render Google-style docstring sections properly: pdoc runs with `-d google` in the Pages workflow, and the markdown docs generator converts `Args:` sections to markdown via `pdoc.docstrings.google` (previously they rendered as flat text or code blocks)
- Normalized docstring `Args:` entries to standard Google style (`period (int): ...` — no space before the colon) across all cython `.pxi` files
- Removed the Cython `embedsignature` directive: docstrings no longer start with a shadow `calc_*` signature line, so generated docs (pdoc and markdown) show only the real function signature. Introspection is unaffected — `binding=True` already provides `inspect.signature` support, and `core.pyi` provides the typed stubs

## 0.0.36
- Replaced tox with nox for multi-version testing (`noxfile.py`; old config archived at `meta/tox.toml`). Sessions install the package via uv, whose built-wheel cache avoids recompiling the Cython extension when the source is unchanged — warm full-matrix runs drop from ~3.5 min to ~25 s. `uv run nox` runs the everyday set; `uv run nox -t full` runs the full pre-publish matrix
- Restored the numpy-only base install: pandas is no longer a hard dependency (it had been re-added inadvertently). Install pandas and/or polars depending on the interfaces you use — the `[pandas]`, `[polars]`, and new `[all]` extras remain available as a convenience; `mintalib.functions` works with numpy alone
- Added `mintalib.utils.normalize_prices` to rename dataframe columns (and the index name for pandas) to lower case; works with pandas and polars via duck typing, no backend import required
- Functions now validate their input and raise useful errors: passing series data to a prices function raises `TypeError: Expected a prices data frame` (was a cryptic `'NoneType' object is not subscriptable`), and series functions require 1D series data — a DataFrame no longer auto-selects the `close` column (use `prices['close']` explicitly; indicators keep the auto-select behavior)
- Removed the undocumented `item` keyword from functions; this also fixes `price(prices, item=...)` silently ignoring the keyword form of its `item` parameter
- README indicators table now includes an Input column (Prices/Series), derived from each core function's first parameter
- RSI now bridges nulls like EMA/RMA: a NaN input no longer resets the previous price, so the price move across a gap is measured (delta taken from the last valid value). Bridging a null is now equivalent to removing it from the series.

## 0.0.35
- Typed the public decorators (`wrap_expression`, `wrap_function`, `wrap_indicator`) with `ParamSpec` so type checkers and editors now resolve the full signatures of `mintalib.expressions`, `mintalib.functions`, and `mintalib.indicators` (parameters, defaults, and return types) instead of `Unknown`. Annotations only — no runtime change.

## 0.0.34
- Released the GIL (`with nogil`) in numerically pure Cython kernels so they run truly in parallel across threads — notably under polars' `map_batches` workers in `mintalib.expressions` (including SMA/EMA/RMA/WMA/SUM/STDEV, MAD, MIN/MAX, CLAG, STREAK, RSI/ROC/LROC, ATR/MFI/SAR, regression, and flag/cross utilities)
- Marked the `core` extension `freethreading_compatible` so it does not force the GIL back on under a free-threaded (`python3.x-t`) interpreter
- Added `tests/test_concurrency.py`: runs every core kernel concurrently across threads (with shared input buffers) and asserts parity with single-threaded results — a concurrency regression guard that also validates free-threading safety when run under a free-threaded interpreter
- Added a free-threaded `3.13t` environment to the tox matrix (pandas-only: polars has no `cp313t` wheel yet); verified the suite — including the concurrency test — passes under a no-GIL CPython build
- Fixed `wrap_expression` to detect multi-output namedtuple results via their `_asdict` method (cleaner namedtuple handling, satisfies strict type checkers)
- Pinned the tox matrix to uv-managed interpreters (`uv_python_preference = "only-managed"`); tox-uv otherwise defaults to `--python-preference system` and could pick a headerless system interpreter, breaking the Cython build

## 0.0.33
- Type stubs (`core.pyi`): multi-output `calc_*` functions now annotated as `-> tuple` (was `-> Any`)
- Added module docstring to `mintalib` for the package overview, visible in `mintalib.__doc__` and in generated docs
- API doc generator now emits type-annotated signatures for `mintalib.core` by reading `core.pyi`
- README cleanup: typo fixes, heading renames (`Polars Expressions` → `Expressions`, `Using Indicators` → `Indicators`), updated multi-output expression note (struct, not tuple), added default-source behavior note for polars expressions
- Renamed `NATR` docstring to "Normalized Average True Range"
- Multi-output `mintalib.expressions` factories (`MACD`, `BBANDS`, `DMI`, `DONCHIAN`, `KELTNER`, `MACDV`, `PPO`, `STOCH`) now return a single polars struct expression aliased to the lowercase indicator name, replacing the previous tuple of field expressions. Use `.struct.unnest()` to flatten or `.struct.field(name)` to pick a field. Breaking change for callers using `*MACD()`-style splatting.
- Optimized rolling-window Cython kernels (SMA, SUM, STDEV, MAD, WMA): eliminated pointer tracking with direct `xs[i - period]` indexing
- Optimized MIN/MAX: compare-to-prior-extremum with rescan-on-expiry, roughly halving the mintalib/talib ratio
- Refactored RSI to use `calc_rma` internally
- Added Cython compiler directives (`boundscheck=False`, `wraparound=False`, `cdivision=True`, `nonecheck=False`)
- Converted codegen and tooling notebooks to plain Python scripts (`make-functions.py`, `make-indicators.py`, `make-expressions.py`, `update-readme.py`, `update-samples.py`)
- Added `test_atr` to `test_vs_talib.py` with convergence check
- Updated bundled sample prices
- Deprecated `mintalib.polars` and `mintalib.pandas` accessor modules (emit `DeprecationWarning` on import)
- Removed `reflib` module (unused pandas/numpy reference implementations)
- Narrowed `mintalib.indicators` to pandas/numpy only — passing a polars DataFrame now raises `TypeError` pointing to `mintalib.expressions`
- Removed undocumented `column_accessor`, `get_series`, `wrap_result` from `mintalib.core` (relocated to `mintalib.model.function` as private helpers backing `wrap_function`)
- Removed `calc_eval` from `mintalib.core` and `eval` from `mintalib.functions`. `mintalib.indicators.EVAL` is preserved as a hand-coded pandas-only `Indicator` class in `mintalib.model.indicator` using `DataFrame.eval`. For polars expression evaluation, use `mintalib.expressions` natively.

## 0.0.31
- Fixed `calc_mad` bug: deviations now use the window mean, first valid index is `period-1`
- Added `ta-lib` as a dev dependency for validation

## 0.0.30
- Added `DONCHIAN` indicator (Donchian Channel)

## 0.0.30
- Added `QuickStudy` and `Trail` studies

## 0.0.29
- Expressions are now uppercase `SMA`, `EMA`, ...

## 0.0.27
- Removed `wrap` parameter from all calc methods

## 0.0.26
- Added a `pandas` extension module `mintalib.pandas`
- Added a `polars` extension module `mintalib.polars`

## 0.0.25
- Added some expression tests
- Added `BBP` Indicator (Bolling Bands Percent)
- Added `BBW` Indicator (Bolling Bands Width)
- Added `MACDV` Indicator (MACD Volatility normalized)
- Modified `STREAK` Indicator. Counts values above zero
- Switched to `tox.toml`

## 0.0.24
- Added polars expressions (experimental)

## 0.0.23
- Refactored indicators as simple wrappers

## 0.0.22
- Added `QSF` Indicator (Quadratic Series Forecast)  

## 0.0.20
- Metadata is passing through to indicators via the `metadata` attribute
- Added `alias` method to FuncIndicator to set indicator output name

## 0.0.19
- Added `STEP` Indicator (Step Function)
- Added `CLAG` Indicator (Confirmation Lag)
- Added `LROC` Indicator (Logarithmic Rate of Change)
- Added `ALMA` Indicator (Arnaud Legoux Moving Average)
- Indicators `ROC` and `LROC` now accept a negative period

## 0.0.18
- Refactored `functions` module to move logic out of core. Function names are now small caps!
- Upper case functions names are legacy and will be removed in the future. Use small caps.

## 0.0.16
- Added `DMI` indicator with grouped calculation for `ADX`, `PDI` and `MDI`
- Renamed `PLUSDI`, `MINUSDI` to `PDI`, `MDI` 

## 0.0.15
- Fixed pypi-readme.md

## 0.0.13
- Added `CURVE` indicator

## 0.0.11
- Added docs

## 0.0.6
- Fixed `MANIFEST.ini`

## 0.0.4
- Indicators moved to `indicators` module
- Functions moved to `functions` module

## 0.0.3
- Functions implemented directly in core
- Setup with pyproject.toml
- Added tox.ini config

## 0.0.1
- Initial release
