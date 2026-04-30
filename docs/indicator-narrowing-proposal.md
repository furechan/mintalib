# Indicator Narrowing Proposal: Pandas-Only Indicators

## Context

This is a prerequisite for [indicator-bridge-proposal.md](indicator-bridge-proposal.md).
`as_expr()` only makes sense once indicators are explicitly pandas-only.

## Current State

`FuncIndicator.__call__` is DataFrame-agnostic. It delegates to two helpers in
`src/mintalib/cython/_common.pxi`:

**`column_accessor(data)`** — accepts pandas DataFrames, polars DataFrames (via
`hasattr(data, 'columns')` duck-typing), polars Struct Series, dicts, and numpy
record arrays.

**`wrap_result(result, source)`** — dispatches on `source.__module__` to wrap a
numpy array result into either a `pd.Series` / `pd.DataFrame` or a
`pl.Series` / `pl.DataFrame`.

This means a polars DataFrame passed to `SMA(20)(df)` silently works today,
returning a polars Series. This is undocumented and untested.

## Constraint

`column_accessor` and `wrap_result` are shared helpers also used by
`src/mintalib/model/function.py` (`wrap_function` decorator), which backs
`mintalib.functions` — a stable interface that intentionally supports both
pandas and polars. These helpers must not be changed.

## Problem

Polars users already have a proper, idiomatic interface in `mintalib.expressions`
that returns `pl.Expr` and integrates with lazy evaluation, `.over()`, and struct
outputs. Indicators running on polars DataFrames bypass all of that and return
eager results with no polars-native features.

Keeping the undocumented polars path in indicators:
- creates an untested, undocumented code path
- blocks a clean implementation of `as_expr()` (which should only bridge to pandas expressions)

## Proposed Change

### `FuncIndicator.__call__`

Add a single guard at the entry point. No code paths change — polars input is
rejected before it ever reaches `column_accessor` or `wrap_result`:

```python
def __call__(self, data):
    import pandas as pd
    if not isinstance(data, (pd.DataFrame, pd.Series, np.ndarray)):
        tname = type(data).__name__
        raise TypeError(
            f"{self.name} indicators only accept pandas DataFrames, Series, or numpy arrays, "
            f"got {tname}. For polars, use mintalib.expressions."
        )
    ...  # rest unchanged
```

`_common.pxi` is not touched — `mintalib.functions` continues to work with both pandas and polars.

## Breaking Change

Any code passing a polars DataFrame or Series to an indicator will get a
`TypeError` with a message pointing to `mintalib.expressions`.

## Scope

- `src/mintalib/model/indicator.py` — `FuncIndicator.__call__` only
- Tests: add a test asserting that passing a polars DataFrame to an indicator raises `TypeError`
- Docs: update `mintalib.indicators` module docstring to say "pandas and numpy only"
