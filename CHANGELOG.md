# Change Log

## 0.0.36
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
