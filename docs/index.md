# Introduction

Minimal technical analysis library for Python

The `mintalib` package offers a curated list of technical analysis indicators implemented in `Cython` for optimal performance. The library is built around `numpy` arrays and works with `pandas` and `polars` DataFrames and Series.


## Interfaces

Mintalib offers three equivalent calculation interfaces for different workflows:

- **Functions** (`mintalib.functions`) — eager functions for NumPy arrays and pandas or polars objects. Names are lower case: `sma`, `ema`, `macd`.
- **Indicators** (`mintalib.indicators`) — composable pandas indicators that bind a calculation with its parameters. Names are upper case: `SMA`, `EMA`, `MACD`.
- **Expressions** (`mintalib.expressions`) — composable expression factories for polars-native workflows. Names are upper case: `SMA`, `EMA`, `MACD`.


## Installation

```console
pip install mintalib
```

Mintalib requires Python 3.11 or newer. Prebuilt `cp311-abi3` wheels are available for regular CPython on Linux (x86_64 and ARM64), macOS (Intel and Apple silicon), and Windows (x64), so supported installations do not need a local compiler chain.

## Quick Start

```python
import mintalib.functions as ta

prices = ...  # pandas DataFrame with open, high, low, close, volume columns

sma = ta.sma(prices['close'], 50)
atr = ta.atr(prices['high'], prices['low'], prices['close'], period=14)
```

## Conventions

Prices DataFrames are expected to have lower case column names `open`, `high`, `low`, `close`, `volume`. If your DataFrame has different column name capitalization you can use the `normalize_prices` utility function to normalize the column names.

