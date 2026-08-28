"""
Minimal technical analysis library for Python.

## Modules

Mintalib exposes eager functions as its primary interface and composable pandas indicators as a secondary interface.

- [mintalib.core](core.md) — core calculation routines implemented in Cython, named `calc_sma`, `calc_ema`, etc.
- [mintalib.functions](functions.md) — plain functions wrapping core routines, named `sma`, `ema`, etc. Primary stable interface.
- [mintalib.indicators](indicators.md) — composable indicator objects for pandas, named `SMA`, `EMA`, etc.

## Naming Conventions

- Core functions use lower case prefixed with `calc_`: `calc_sma`, `calc_ema`, `calc_macd`
- Functions use lower case: `sma`, `ema`, `macd`
- Indicators use upper case: `SMA`, `EMA`, `MACD`

## Input Parameters

- `series` — a pandas Series or NumPy array (single column input)
- `prices` — a pandas DataFrame with columns `open`, `high`, `low`, `close`, `volume` (all lower case)

## Multi-Output Indicators

Indicators with multiple outputs (e.g. `MACD`, `BBANDS`) return named tuples from
`mintalib.core` and `mintalib.functions`, and DataFrames from `mintalib.indicators`.
"""

__pdoc__ = {"builder": False, "testing": False}
