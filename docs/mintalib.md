# mintalib

Minimal technical analysis library for Python.

## Modules

- [mintalib.core](mintalib.core.md) — core calculation routines implemented in Cython, named `calc_sma`, `calc_ema`, etc.
- [mintalib.functions](mintalib.functions.md) — plain functions wrapping core routines, named `sma`, `ema`, etc. Primary stable interface.
- [mintalib.indicators](mintalib.indicators.md) — composable indicator objects for pandas and numpy, named `SMA`, `EMA`, etc.
- [mintalib.expressions](mintalib.expressions.md) — polars expression factories, named `SMA`, `EMA`, etc.

## Naming Conventions

- Core functions use lower case prefixed with `calc_`: `calc_sma`, `calc_ema`, `calc_macd`
- Functions use lower case: `sma`, `ema`, `macd`
- Indicators and Expressions use upper case: `SMA`, `EMA`, `MACD`

## Input Parameters

- `series` — a pandas/polars series or numpy array (single column input)
- `prices` — a pandas or polars DataFrame with columns `open`, `high`, `low`, `close`, `volume` (all lower case)

## Multi-Output Indicators

Indicators with multiple outputs (e.g. `MACD`, `BBANDS`) return:

- named tuples from `mintalib.core` and `mintalib.functions`
- tuples of expressions in `mintalib.expressions`
- polars structs in the polars accessor
