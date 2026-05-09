# Narrowing Plan: Pandas-Only Indicators + Helper Relocation

Two-step plan to narrow `mintalib.indicators` to pandas/numpy only, then move the polyvalent conversion helpers out of the Cython core into the functions namespace.

Supersedes [indicator-narrowing-proposal.md](indicator-narrowing-proposal.md) (which proposed only a single type guard at the indicator entry point). This plan goes further: replaces the duck-typed shared helpers with typed pandas code on the indicator side, then relocates the now-unused-by-indicators helpers out of `core`.

## Goals

- `mintalib.indicators` becomes pandas-only (`pd.DataFrame`, `pd.Series`, `np.ndarray`).
- `mintalib.expressions` stays polars-only (already is).
- `core.calc_*` stays numpy-level.
- `mintalib.functions` stays polyvalent — legacy, contract unchanged.

## Step 1 — Make Indicators Pandas-Only

### Code

`src/mintalib/model/indicator.py`:
- Add `import pandas as pd` at top.
- Drop `from ..core import column_accessor, get_series, wrap_result`.
- Replace with inline typed helpers:
  - `_get_series(data, item)` — `data[item or 'close'] if isinstance(data, pd.DataFrame) else data`.
  - `_wrap_result(result, source, name)` — typed `pd.Series` / `pd.DataFrame` returns using `source.index`.
- Inline the `Indicator.get_series` base-class method the same way.
- Add an input-type guard at `FuncIndicator.__call__`: reject anything that isn't `pd.DataFrame | pd.Series | np.ndarray` with a `TypeError` pointing to `mintalib.expressions` for polars use cases.

### Tests
- Assert passing a polars DataFrame to an indicator raises `TypeError`.
- Existing pandas/numpy indicator tests should pass unchanged.

### Docs
- Update `mintalib.indicators` module docstring to state "pandas and numpy only".
- `CLAUDE.md` project conventions already say "indicators ... work with pandas and numpy"; no change needed.

### Breaking change
- Polars input to indicators was an undocumented, untested code path. Now explicitly rejected.

## Step 2 — Relocate Helpers from Core to Functions Namespace

After step 1, `model/function.py` is the sole consumer of `column_accessor`, `get_series`, `wrap_result`.

### Code

- Move `column_accessor`, `get_series`, `wrap_result` from `src/mintalib/cython/_common.pxi` into the top of `src/mintalib/model/function.py`, as a prelude to `wrap_function`.
- Move as-is, no logic changes — `functions` stays polyvalent, so the `sys.modules` lookup and `source.__module__` dispatch still earn their keep.
- Drop the import of these names from `mintalib.core` in `model/function.py`.

### Cleanup

- `_common.pxi` keeps only `check_size` and `add_metadata` (genuinely Cython-adjacent).
- `core.pyi` reduces to `calc_*` only.
- `scripts/make-stubs.py` `HELPERS = [...]` carve-out (line 44) goes away.
- Editing these helpers no longer triggers `inv make`.

### Breaking change
- `mintalib.core.column_accessor` / `get_series` / `wrap_result` were never documented as public API but were technically importable. They are no longer in `core` after this step.
- Add a one-line CHANGELOG entry: "removed undocumented `column_accessor`, `get_series`, `wrap_result` from `mintalib.core`".

## Out of Scope

- No splitting of helpers into per-module copies. Indicators get inline typed pandas code; functions keeps the polyvalent helpers. No duplication across modules.
- No changes to the `mintalib.functions` contract. If/when functions is itself narrowed or retired, the helpers go with it.
- No changes to expressions, polars accessor, or pandas accessor.
