"""
Minimal technical analysis library for Python.

## Modules

Every indicator is available in all three stable interfaces (functions, indicators, expressions) — enforced by the test suite.

- [mintalib.core](core.md) — core calculation routines implemented in Cython, named `calc_sma`, `calc_ema`, etc.
- [mintalib.functions](functions.md) — plain functions wrapping core routines, named `sma`, `ema`, etc. Primary stable interface.
- [mintalib.indicators](indicators.md) — composable indicator objects for pandas, named `SMA`, `EMA`, etc.
- [mintalib.expressions](expressions.md) — polars expression factories, named `SMA`, `EMA`, etc.

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
- polars struct expressions in `mintalib.expressions` (unpack with `.struct.unnest()` or pick a field with `.struct.field(name)`)
"""

__pdoc__ = {"builder": False, "testing": False}
