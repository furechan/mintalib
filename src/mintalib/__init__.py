"""
Minimal technical analysis library for Python.

## Modules

Mintalib exposes equivalent eager, pandas-composable, and polars-expression interfaces.

- [mintalib.core](core.md) — core calculation routines implemented in Cython, named `calc_sma`, `calc_ema`, etc.
- [mintalib.functions](functions.md) — eager functions wrapping core routines, named `sma`, `ema`, etc.
- [mintalib.indicators](indicators.md) — composable indicator objects for pandas, named `SMA`, `EMA`, etc.
- [mintalib.expressions](expressions.md) — composable expression factories for polars, named `SMA`, `EMA`, etc.

## Naming Conventions

- Core functions use lower case prefixed with `calc_`: `calc_sma`, `calc_ema`, `calc_macd`
- Functions use lower case: `sma`, `ema`, `macd`
- Indicators use upper case: `SMA`, `EMA`, `MACD`
- Expressions use upper case: `SMA`, `EMA`, `MACD`

## Input Parameters

- `series` — a pandas or polars Series, or NumPy array (single column input)
- `prices` — a pandas or polars DataFrame with columns `open`, `high`, `low`, `close`, `volume` (all lower case)

## Multi-Output Indicators

Indicators with multiple outputs (e.g. `MACD`, `BBANDS`) return named tuples from
`mintalib.core` and `mintalib.functions`, and DataFrames from `mintalib.indicators`.
"""

__pdoc__ = {"builder": False, "testing": False}
