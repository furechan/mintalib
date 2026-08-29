# Mintalib

Minimal technical analysis library for Python.

This package offers a curated list of technical analysis indicators implemented in `Cython` for optimal performance. The library is built around `numpy` arrays and integrates with `pandas` DataFrames and Series.

!!! warning
    This project is experimental and the interface is likely to change.

## Interfaces

Mintalib offers three equivalent calculation interfaces for different workflows:

- **Functions** (`mintalib.functions`) — eager functions for NumPy arrays and pandas or polars objects. Names are lower case: `sma`, `ema`, `macd`.
- **Indicators** (`mintalib.indicators`) — composable pandas indicators that bind a calculation with its parameters. Names are upper case: `SMA`, `EMA`, `MACD`.
- **Expressions** (`mintalib.expressions`) — composable expression factories for polars-native workflows. Names are upper case: `SMA`, `EMA`, `MACD`.

Functions and indicators have example notebooks:

- [Functions](examples/functions.ipynb)
- [Indicators](examples/indicators.ipynb)

Polars expressions are documented in the [Expressions reference](reference/expressions.md).

## Installation

```console
pip install mintalib
```

Mintalib requires Python 3.11 or newer. Prebuilt `cp311-abi3` wheels are available for regular CPython on Linux (x86_64 and ARM64), macOS (Intel and Apple silicon), and Windows (x64), so supported installations do not need a local C compiler.

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
- [mintalib.expressions](reference/expressions.md) — polars expression factories
- [mintalib.core](reference/core.md) — low-level calculation routines
