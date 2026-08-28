# Mintalib

Minimal technical analysis library for Python.

This package offers a curated list of technical analysis indicators implemented in `Cython` for optimal performance. The library is built around `numpy` arrays and integrates with `pandas` DataFrames and Series.

!!! warning
    This project is experimental and the interface is likely to change.

## Interfaces

Mintalib offers two interfaces for different workflows:

- **Functions** (`mintalib.functions`) — concrete functions for arrays and pandas objects. Names are lower case: `sma`, `ema`, `macd`.
- **Indicators** (`mintalib.indicators`) — pandas-only composable indicators that bind an indicator with its calculation parameters. Names are upper case: `SMA`, `EMA`, `MACD`.

The primary interfaces have example notebooks:

- [Functions](examples/functions.ipynb)
- [Indicators](examples/indicators.ipynb)

## Installation

```console
pip install mintalib
```

## Quick Start

```python
import mintalib.functions as ta

prices = ...  # pandas DataFrame with open, high, low, close, volume columns

sma = ta.sma(prices['close'], 50)
atr = ta.atr(prices, 14)
```

## Conventions

Prices DataFrames are expected to have lower case column names `open`, `high`, `low`, `close`, `volume`. If your DataFrame has different column name capitalization you can use the `normalize_prices` utility function to normalize the column names.

## Reference

- [mintalib](reference/index.md) — package overview
- [mintalib.functions](reference/functions.md) — calculation functions
- [mintalib.indicators](reference/indicators.md) — pandas indicators
- [mintalib.core](reference/core.md) — low-level calculation routines
