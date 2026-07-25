# Mintalib

Minimal technical analysis library for Python.

This package offers a curated list of technical analysis indicators implemented in `Cython` for optimal performance. The library is built around `numpy` arrays and offers a variety of interfaces for `pandas` and `polars` dataframes and series.

!!! warning
    This project is experimental and the interface is likely to change.

## Interfaces

Mintalib offers three interfaces for different workflows:

- **Functions** (`mintalib.functions`) — concrete functions compatible with both polars and pandas. Names are lower case: `sma`, `ema`, `macd`.
- **Polars Expressions** (`mintalib.expressions`) — composable polars expression factory methods, best for polars-native workflows. Names are upper case: `SMA`, `EMA`, `MACD`.
- **Pandas Indicators** (`mintalib.indicators`) — pandas-only composable indicators that bind an indicator with its calculation parameters. Names are upper case: `SMA`, `EMA`, `MACD`.

Each interface has an example notebook:

- [Functions](examples/functions.ipynb)
- [Expressions](examples/expressions.ipynb)
- [Indicators](examples/indicators.ipynb)

## Installation

```console
pip install mintalib
```

## Quick Start

```python
import mintalib.functions as ta

prices = ...  # pandas/polars DataFrame with open, high, low, close, volume columns

sma = ta.sma(prices['close'], 50)
atr = ta.atr(prices, 14)
```

## Conventions

Prices data frames (either pandas or polars) are expected to have lower case column names `open`, `high`, `low`, `close`, `volume`. If your dataframe has different column name capitalization you can use the `normalize_prices` utility function to normalize the column names.

## Reference

- [mintalib](reference/index.md) — package overview
- [mintalib.functions](reference/functions.md) — calculation functions
- [mintalib.expressions](reference/expressions.md) — polars expressions
- [mintalib.indicators](reference/indicators.md) — pandas indicators
- [mintalib.core](reference/core.md) — low-level calculation routines
