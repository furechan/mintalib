# Minimal Technical Analysis Library for Python


This package offers a curated list of technical analysis indicators implemented in cython. It is built around `numpy` arrays and aims to be compatible with `pandas` and also `polars` where applicable.
The library is pre-compiled with `cython` so as not to require the `cython` runtime at installation. Also it does not link with `numpy` and so avoids binary dependency issues.


> **Warning**
> This project is experimental and the interface can change.
> For a similar project with a mature api you may want to look into
> [ta-lib](https://pypi.org/project/TA-Lib/).



## Structure
The `mintalib` package contains three main modules:

- [mintalib.core](/docs/mintalib.core.md)
    low level calculation rountines implemented in cython
- [mintalib.functions](/docs/mintalib.functions.md)
    wrapper functions to compute indicators
- [mintalib.indicators](/docs/mintalib.indicators.md)
    composable interface to indicators

Most calculations are available in three flavors.
- The raw calculation routine is called something like
`calc_sma` and is available from the `mintalib.core` module. This routine is implemented in cython.
- A function called something like `SMA` is also available from the `mintalib.functions` module, and includes extra facilities like selection of column (`item`) and wrapping of results.
- Finally an indicator with the same name `SMA` is available from the `mintalib.indicators` and offers a composable interface.


## List of Indicators

| Name       | Description                              |
|:-----------|:-----------------------------------------|
| ADX        | Average Directional Index                |
| ATR        | Average True Range                       |
| AVGPRICE   | Average Price                            |
| BBANDS     | Bollinger Bands                          |
| BOP        | Balance of Power                         |
| CCI        | Commodity Channel Index                  |
| CMF        | Chaikin Money Flow                       |
| CROSSOVER  | Cross Over                               |
| CROSSUNDER | Cross Under                              |
| CURVE      | Curve (time curvilinear regression)      |
| DEMA       | Double Exponential Moving Average        |
| DIFF       | Difference                               |
| DMI        | Directional Movement Indicator           |
| EMA        | Exponential Moving Average               |
| EVAL       | Expression Eval (pandas only)            |
| EXP        | Exponential                              |
| FLAG       | Flag for value above zero                |
| FORECAST   | Forecast (time linear regression)        |
| HMA        | Hull Moving Average                      |
| KAMA       | Kaufman Adaptive Moving Average          |
| KELTNER    | Keltner Channel                          |
| KER        | Kaufman Efficiency Ratio                 |
| LAG        | Lag Function                             |
| LOG        | Logarithm                                |
| MA         | Generic Moving Average                   |
| MACD       | Moving Average Convergenge Divergence    |
| MAD        | Mean Absolute Deviation                  |
| MAX        | Rolling Maximum                          |
| MDI        | Minus Directional Index                  |
| MFI        | Money Flow Index                         |
| MIDPRICE   | Mid Price                                |
| MIN        | Rolling Minimum                          |
| NATR       | Average True Range (normalized)          |
| PDI        | Plus Directional Index                   |
| PPO        | Price Percentage Oscillator              |
| PRICE      | Generic Price                            |
| RMA        | Rolling Moving Average (RSI style)       |
| ROC        | Rate of Change                           |
| RSI        | Relative Strength Index                  |
| RVALUE     | RValue (time linear regression)          |
| SAR        | Parabolic Stop and Reverse               |
| SIGN       | Sign                                     |
| SLOPE      | Slope (time linear regression)           |
| SMA        | Simple Moving Average                    |
| STDEV      | Standard Deviation                       |
| STOCH      | Stochastic Oscillator                    |
| STREAK     | Consecutive streak of ups or downs       |
| SUM        | Rolling Sum                              |
| TEMA       | Triple Exponential Moving Average        |
| TRANGE     | True Range                               |
| TYPPRICE   | Typical Price                            |
| UPDOWN     | Flag for value crossing up & down levels |
| WCLPRICE   | Weighted Close Price                     |
| WMA        | Weighted Moving Average                  |


## Using Functions

Functions are available via the `functions` module,
with names like `SMA`, `EMA`, `RSI`, `MACD`, all in **upper case**.
The first parameter of a function is either `prices` or `series` depending on whether
the functions expects a dataframe of prices or a single series.
Functions that expect series data can be applied to a prices dataframe, in which case they use 
the column specified with the `item` parameter or by default the `close` column.

A `prices` dataframe can be a pandas dataframe, a polars dataframe or a dictionary of numpy arrays.
The column names for prices are expected to include `open`, `high`, `low`, `close` all in **lower case**.
A `series` can be a pandas series, a polars series or any iterable compatible with numpy arrays.

Functions automatically wrap their result to match their input, so that for example 
pandas based inputs will yield pandas based results with a matching index.


```python
import yfinance as yf

from mintalib.functions import SMA, MAX

# fetch prices (eg with yfinance)
prices = yf.Ticker('AAPL').history('5y')

# convert column and index names to lower case
prices = prices.rename(columns=str.lower).rename_axis(index=str.lower)

# compute indicators
sma50 = SMA(prices, 50)  # SMA of 'close' with period = 50
sma200 = SMA(prices, 200)  # SMA of 'close' with period = 200
high200 = MAX(prices, 200, item='high')  # MAX of 'high' with period = 200

```


## Using Indicators

Indicators are available via the `indicators` module, with similar names as functions all in **uper case**.

Indicators offer a composable interface where a function is bound with its calculation parameters. When instantiated with parameters an indicator yields a callable that can be applied to prices or series data. Indicators support the `@` operator as syntactic sugar to apply the indicator to data. So for example `SMA(50) @ prices` can be used to compute the 50 period simple moving average on `prices`, insted of `SMA(50)(prices)`.

```python
sma50 = SMA(50) @ prices
sma200 = SMA(200) @ prices
```

The `@` operator can also be used to compose indicators, where for example `ROC(1) @ EMA(20)` means `ROC(1)` applied to `EMA(20)`.

```python
slope = ROC(1) @ EMA(20) @ prices
```


## Using Indicators with Pandas

Prices indicators like `ATR` can only be applied to prices dataframes.

```python
atr = ATR(14) @ prices
```

Series indicators can be applied to a prices dataframe or a series. When applied to prices you must specify a column with the `item` or otherwize the indicator will use the `"close"` column by default.

```python
# SMA on the close column
sma50 = SMA(50) @ prices

# SMA on the volume column
vol50 = SMA(50, item="volume") @ prices

# Which is the same as
vol50 = SMA(50) @ prices.volume 
``` 

With pandas dataframes you can compose and assign multiple indicators in one call using the builtin `assign` method.


```python
import yfinance as yf

from mintalib.indicators import EMA, SMA, ROC, RSI, EVAL

# fetch prices (eg with yfinance)
prices = yf.Ticker('AAPL').history('5y')

# convert column and index names to lower case
prices = prices.rename(columns=str.lower).rename_axis(index=str.lower)

# compute and append indicators to prices
# note that calculations can use results from prior indicators
result = prices.assign(
    sma50 = SMA(50),
    sma200 = SMA(200),
    rsi = RSI(14),
    slope = ROC(1) @ EMA(20),
    uptrend = EVAL("sma50 > sma200")
)
```


## Using Indicators with Polars

Indicators can be applied to polars prices dataframes and series in the same way as with pandas. 

The `@` operator has been extended to also work with polars expressions. This is just syntactic sugar around polars `map_batches`.

In the following example, you can assign multiple columns using polars `with_columns`.

```python
import polars as pl
from polars import col

import yfinance as yf

from mintalib.indicators import EMA, SMA, ROC, RSI, EVAL

# fetch prices (eg with yfinance)
prices = yf.Ticker('AAPL').history('5y')

# convert column and index names to lower case
prices = prices.rename(columns=str.lower).rename_axis(index=str.lower)

# convert to polars dataframe 
prices = pl.from_pandas(prices, include_index=True)

# compute and append indicators to prices
result = prices.with_columns(
    sma20 = SMA(20) @ col('close'),
    sma50 = SMA(50) @ col('close'),
)
```


## Example Notebooks

You can find example notebooks in the `examples` folder. 


## Installation

You can install the current version of this package with pip

```console
python -mpip install git+https://github.com/furechan/mintalib.git
```

## Dependencies

- python >= 3.9
- pandas
- numpy


## Related Projects
- [ta-lib](https://github.com/mrjbq7/ta-lib) Python wrapper for TA-Lib
- [qtalib](https://github.com/josephchenhk/qtalib) Quantitative Technical Analysis Library
- [numpy](https://github.com/numpy/numpy) The fundamental package for scientific computing with Python
- [pandas](https://github.com/pandas-dev/pandas) Flexible and powerful data analysis / manipulation library for Python
- [polars](https://github.com/pola-rs/polars) Fast multi-threaded, hybrid-out-of-core query engine focussing on DataFrame front-ends
- [yfinance](https://github.com/ranaroussi/yfinance) Download market data from Yahoo! Finance's API


