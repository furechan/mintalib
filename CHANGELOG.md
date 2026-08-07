# Change Log

## 0.1.5
- Narrowed `mintalib.studies` to pandas-only, aligning it with the indicators decision from 0.1.4 (pandas for `indicators`/`studies`, native `expressions` for polars). The module predated that split — `QuickStudy` and `Trail` still carried `detect_backend` dispatch and `apply_polars` branches. Those are gone: each study's `__call__` now validates `isinstance(prices, pd.DataFrame)` and raises the standard `TypeError` pointing polars users to `mintalib.expressions`. Also annotated the `Study` hierarchy (`-> Any` on the abstract `__call__` — `ChainedStudy` can pipe into arbitrary callables — and `-> pd.DataFrame` on the concrete studies), fixing the pyright inferred-`None` override error. The module remains unexported and untested (experimental)
- The `indicators`, `expressions`, and `studies` module docstrings now state their backend up front ("This module is pandas-only / polars-only ..."), replacing the input-types note buried at the bottom of the indicators docstring (docstring changes made in the generator preludes and regenerated, with `docs/reference/` refreshed via `inv docs`)
- Playground notebooks now follow a naming convention keyed to their ty blind spots: notebooks with `%%cython` magic cells carry "cython" in the name (`filter-vs-vector`, `slope-proto`, `curve-proto` renamed with a `cython-` prefix), notebooks using the registered `ts` accessors carry "accessor". The blanket (and disabled) ty override for `playground--/**` is replaced by two narrow ones: `unresolved-reference` ignored only in `*cython*.ipynb`, `unresolved-attribute` only in `*accessor*.ipynb` — all other playground notebooks are fully checked
- Ported `scripts/make-api-docs.py` from pdoc to griffe (matching mplchart): griffe's static analysis provides module structure, source order, exports, and variable docstrings (string literals after assignments, invisible at runtime), plus its google docstring parser; function docstrings and signatures still come from the live objects via `inspect`, since the wrapper decorators attach them at runtime. The `mintalib.core` path (signatures from the `.pyi` stub via `ast`) is unchanged. Output markdown is content-identical apart from whitespace normalization and two fixes surfaced by the port: `roc`/`lroc` docstrings had a continuation line at the wrong indent (pdoc rendered it as a bogus extra list item; griffe correctly rejects it), and `annotate_parameter` in `builder.py` gained a `float`/`double` case, so `calc_step`'s `threshold` is now annotated `float` instead of the string `'float'` in all generated stubs. `pdoc` removed from dev dependencies, `griffe` added
- Split dependency-groups into `dev` and `docs` (mkdocs-material, mkdocs-jupyter), matching the mplchart convention, with `tool.uv.default-groups = ["dev", "docs"]` so plain `uv sync` still installs both. The Pages workflow now runs `uv sync --only-group docs` + `uv run --no-sync mkdocs build` — deploys no longer compile the Cython extension or install the dev stack, since the site only renders committed markdown and pre-executed notebooks. `pdoc` stays in `dev` (it backs the `make-api-docs.py` codegen, not the site build). Removed the legacy `tool.pydev` section
- Type-checker cleanup in the model layer and accessors, static-only by policy: `__signature__` is set via `setattr(wrapper, ...)` instead of direct assignment with ignore comments; namedtuple detection standardized on the `getattr(result, "_asdict", None)` probe (replacing `isinstance(result, tuple) and hasattr(...)`, which pyright can't narrow) across `model/function.py`, `model/indicator.py`, `pandas.py`, and `polars.py`; and `cast(pd.Series, ...)` on DataFrame column access in `model/indicator.py`, where pandas 3.0's unannotated `DataFrame.__getitem__` makes pyright infer `Series | Unknown | DataFrame`

## 0.1.4
- Split the indicator model by output kind: `SeriesIndicator` (60 single-output indicators, `__call__` typed `-> pd.Series`) and `FrameIndicator` (the 8 multi-output ones — BBANDS, DMI, DONCHIAN, KELTNER, MACD, MACDV, PPO, STOCH — typed `-> pd.DataFrame`), both under the existing `Indicator` base. `make-indicators.py` picks the wrapper (`wrap_series_indicator` / `wrap_frame_indicator`, replacing `wrap_indicator`) from the core function's `output_names` metadata. New: `MACD()["macd"]` selects one output of a multi-output indicator as a series indicator, composing with `.alias()`, `.as_expr()`, and chains. `as_expr()` signatures are now exact — no argument on series indicators, required `item` on frame indicators (`MACD().as_expr("macd")` unchanged) — so the old runtime arity guards (`TypeError` on multi-output without item, `ValueError` for item on single-output) became signature-level errors; unknown output columns now raise `KeyError` from `__getitem__`. `alias()` moved to `SeriesIndicator` (aliasing a multi-output result, formerly a runtime `ValueError`, is no longer expressible). `output_names` now exists only on frame indicators (non-Optional); chains split into `SeriesIndicatorChain`/`FrameIndicatorChain` under the `IndicatorChain` base, with the chain's kind determined by its last element — `TYPPRICE() | BBANDS(20)` is a `FrameIndicator` and supports `["upperband"]`
- Typed `Indicator.__call__` (and its concrete implementations) as `data: pd.DataFrame | pd.Series | np.ndarray` → `pd.Series | pd.DataFrame`. Previously the abstract method was unannotated, so Pylance inferred every indicator result as `None` — e.g. `ATR(14)(prices)` typed as `None`, and `prices.apply(SMA(20))` failed overload resolution against the pandas stubs. The indicator result wrapper now raises `TypeError` on an unexpected calc result type instead of silently passing it through — an unreachable branch in practice, since every core calc routine returns an ndarray or a namedtuple (the passthrough in `model/function.py` is unchanged: it is what makes the functions interface backend-preserving for numpy input)

## 0.1.3
- Added PyPI project urls: `documentation` (the mkdocs site), `repository`, and `changelog` alongside the existing `homepage`

## 0.1.2
- Replaced the manually-refreshed interface coverage table (`output/coverage.md` and `scripts/make-coverage.py`, removed) with `tests/test_coverage.py`, which asserts every core `calc_*` routine is exposed in all three stable interfaces — previously each test file enumerated from its own module, so a codegen omission would have passed silently, and the table had gone stale. The guarantee is now stated on the reference index page instead
- Removed the pypi-readme indirection: `pyproject.toml` now points `readme` at `README.md` directly, `output/pypi-readme.md` is deleted, and `update-readme.py` no longer rewrites repo-relative links (the README has none). Instead, a new `scripts/check-readme.py` fails `inv build` if repo-relative links ever reappear (PyPI renders the readme without repo context) — use absolute URLs in the README
- Docs site is now built with mkdocs-material instead of pdoc: the GitHub Pages workflow runs `mkdocs build` over the `docs/` tree — hand-written homepage (`docs/index.md`), the `examples/` notebooks rendered via mkdocs-jupyter (linked into the site through a `docs/examples` symlink), and the generated markdown API reference (moved from `docs/*.md` to `docs/reference/`). pdoc remains a dependency of `scripts/make-api-docs.py` only (docstring parsing/introspection). `inv docs --serve` regenerates the reference and serves the site locally. The reference generator now emits name-only headings (with the signature on its own line below) and renders docstring sections like `Arguments:` as bold text instead of headings, so the page table of contents shows clean indicator names
- `sample_prices` now has overloaded type annotations keyed on the `backend` literal (pandas/polars imported under `TYPE_CHECKING` only — no new runtime dependency), with caching delegated to an inner `@lru_cache` helper so all checkers resolve the overloads. Previously the inferred `pd.DataFrame | pl.DataFrame` union made Pylance report `Object of type "Series[Any]" is not callable` on every `prices.select(...)` in the notebooks (pandas-stubs types `DataFrame.__getattr__` as returning `Series[Any]`); the caching behavior is unchanged
- Removed `sample_dataset` (and the `SAMPLE_TICKERS` constant): added April 2026 for `.over()` benchmarking but never referenced anywhere; the equivalent tooling lives in bearta's own samples module
- Reworked the example notebooks into proper walkthroughs (they double as the site's Examples section). Fixed stale broken cells in `functions.ipynb` — `ta.sma(prices, 20)` / `ta.macd(prices, ...)` passed a DataFrame to series functions, which raises since implicit `close` selection was removed in 0.0.36. New coverage: prices-vs-series and builtin-shadowing gotchas, backend-preserving outputs (functions); `src=` column names, output naming and `.alias()`, `.struct.field()`, lazy frames and `.over()` window usage (expressions); `item=`, series/numpy inputs, chaining and `.alias()`, `EVAL` and sequential `assign`, multi-output joins, and pandas 3.0 `as_expr()` (indicators). All notebooks re-executed
- Breaking: renamed `MIDPRICE` to `MEDPRICE` (core function `calc_midprice` → `calc_medprice`) across all interfaces, following the established convention where (high + low) / 2 is the median price (talib `MEDPRICE`; talib `MIDPRICE` is a different, period-based indicator). The `PRICE` item shortcut `'mid'` is renamed to `'med'` accordingly (`'hl2'` unchanged). Clean break, no deprecation aliases
- Breaking: the BBANDS family (`BBANDS`, `BBP`, `BBW`, core functions `calc_bbands`, `calc_bbp`, `calc_bbw`) now takes a series instead of a prices DataFrame, defaulting to the `close` column — the standard Bollinger definition matching TA-Lib (previously computed internally from typical price). Use `item=` (indicators) or `src=` (expressions) to select another price source; the old typical-price behavior is `TYPPRICE() | BBANDS(20)` (indicators) or `BBANDS(20, src=TYPPRICE())` (expressions). BBANDS is now covered by the TA-Lib parity tests

## 0.1.1
- Reverted nox back to tox (tox-uv): declarative config fits this repo; same everyday set plus `tox -m full` for the full matrix (3.10-3.14, 3.13t); no PATH shims (tox-uv provisions via the uv store)
- noxfile now sets `UV_PYTHON_INSTALL_BIN=0` so nox's interpreter provisioning (`uv python install`) no longer symlinks `python3.X` executables into `~/.local/bin`; uv-managed pythons stay in uv's store, off PATH
- Added `ZLEMA` (Zero-Lag Exponential Moving Average, core function `calc_zlema`): an EMA applied to the de-lagged series `2 * value - value[lag]` with `lag = (period - 1) // 2`, available across all interfaces (functions, indicators, expressions)
- Expression factories now type-check when used with `Expr.pipe` (e.g. `EMA(20).pipe(ROC, 1)`): `wrap_expression` is annotated to return an `ExprFactory` protocol declaring both call conventions — the classic keyword form and the pipe form with a leading positional expression as `src`. Annotation-only change, no runtime behavior difference
- Fixed precision degradation in the LINREG/QUADREG kernels on long series: the rolling sums used the absolute bar index as x, so the quadratic statistics decayed to noise past ~10k bars and overflowed to nan near 1M bars (the linear ones lost ~8 digits). Both kernels now use the anchored one-pass pattern from barcalc (x anchored to a periodically reset origin, with a bounded rewind), plus precomputed pure-x moments on the fixed window grid — QUADREG on a centered grid where the linear and quadratic terms are orthogonal, which also removes the ill-conditioned normal-equations denominator. Worst-case error at 1M bars is now ~1e-11 (curve) with no measurable performance cost (~7 ms per 1M bars); `tests/test_regression.py` gains a long-series precision test that fails on the old kernels

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
