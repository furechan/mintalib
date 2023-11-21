# Minimal Technical Analysis Library for Python


This library offers a curated list of technical analysis indicators
implemented in cython.
It is built around `numpy` arrays and aims to be compatible
with both `pandas` and `polars` dataframes where possible.


> **Warning**
> This is work in progress.
> For a similar project with a mature api
> you may want to look at [ta-lib](https://pypi.org/project/TA-Lib/).


## Structure
The `mintalib` package contains three main modules:
- `mintalib.core` low level calculation rountines implemented in cython
- `mintalib.functions` single use functions to compute indicators
- `mintalib.indicators` composable interface to indicators

## Functions

Indicators are available as simple functions via the `functions` module,
with names like `SMA`, `EMA`, `RSI`, `MACD`, all in **upper case**.
The first parameter of a function is either `prices` or `series` depending on whether
the functions expects a dataframe of prices or a single series.
Functions that expect series data can still be applied to prices data, in which case they use 
the `close` column by default or otherwize the column specified with the `item` parameter.

A `prices` dataframe can be a pandas dataframe, a polars dataframe or a dictionary of numpy arrays.
The column names for prices are expected to include `open`, `high`, `low`, `close` all in **lower case**.
A `series` can be a pandas series, a polars series or any iterable compatible with numpy arrays.

Functions attempt to wrap their result to match their input, so that for example 
pandas based inputs will yield pandas based results with matching index.


```python
import yfinance as yf

from mintalib.functions import SMA, MAX

# fetch prices (eg with yfinance)
prices = yf.Ticker('AAPL').history('5y')

# convert column names to lower case
prices = prices.rename(columns=str.lower).rename_axis(index=str.lower)

# compute indicators
sma50 = SMA(prices, 50)  # SMA of 'close' with period = 50
sma200 = SMA(prices, 200)  # SMA of 'close' with period = 200
high200 = MAX(prices, 200, item='high')  # MAX of 'high' with period = 200

```


## Composable Interface

Indicators are also available through a composable interface via the `indicators` module,
with similar the same names all in **uper case**.
Each indicator is implemented as a class to be instanciated with calculation parameters.
The instance objects are callables that can be applied to series or prices data like regular functions. 
So for example `SMA(50)` is a callable object that will return the 50 period simple moving average of its argument.

Indicators can be composed with the `@` operator,
where for example `EMA(20) @ ROC(5)` means `EMA(20)` applied to `ROC(5)`.
The same `@` operator can also be used to apply an indicator to some data,
where for example `SMA(50) @ prices` can be used to compute the 50 period simple moving average on `prices`. 

Please note that with pandas dataframes you can compose and assign multiple indicators in one go
using the builtin `assign` method.

```python
import yfinance as yf

from mintalib.indicators import EMA, SMA, ROC, RSI, SLOPE, EVAL

# fetch prices (eg with yfinance)
prices = yf.Ticker('AAPL').history('5y')

# convert column names to lower case
prices = prices.rename(columns=str.lower).rename_axis(index=str.lower)

# compute and append indicators to prices
result = prices.assign(
    sma50 = SMA(50),
    sma200 = SMA(200),
    rsi = RSI(14),
    slope = SLOPE(20),
    trend = EMA(20) @ ROC(5),
    pos = EVAL("sma50 > sma200")
)

# you will notice that the EVAL expression at the end
# can use the names sma50 and sma200 that where defined
# just above in the same function call!
```


## Examples

You can find example notebooks in the examples folder. 


## Installation

You can install the current version of this package with pip
```console
python -mpip install git+https://github.com/furechan/mintalib.git
```

## Related Projects
- [ta-lib](https://github.com/mrjbq7/ta-lib) Python wrapper for TA-Lib
- [qtalib](https://github.com/josephchenhk/qtalib) Quantitative Technical Analysis Library
- [numpy](https://github.com/numpy/numpy) The fundamental package for scientific computing with Python
- [pandas](https://github.com/pandas-dev/pandas) Flexible and powerful data analysis / manipulation library for Python
- [polars](https://github.com/pola-rs/polars) Fast multi-threaded, hybrid-out-of-core query engine focussing on DataFrame front-ends
- [yfinance](https://github.com/ranaroussi/yfinance) Download market data from Yahoo! Finance's API

## List of Indicators

| Name             | Description                               |
|:-----------------|:------------------------------------------|
| ADX              | Average Directional Index                 |
| ATR              | Average True Range                        |
| AVGPRICE         | Average Price                             |
| BBANDS           | Bollinger Bands                           |
| BOP              | Balance of Power                          |
| CCI              | Commodity Channel Index                   |
| CMF              | Chaikin Money Flow                        |
| CROSSOVER        | Cross Over                                |
| CROSSUNDER       | Cross Under                               |
| CURVE            | Curve (time curvilinear regression)       |
| DEMA             | Double Exponential Moving Average         |
| DIFF             | Difference                                |
| EFFICIENCY_RATIO | Efficiency Ratio (Kaufman)                |
| EMA              | Exponential Moving Average                |
| EVAL             | Expression Eval (pandas only)             |
| EXP              | Exponential                               |
| FLAG_ABOVE       | Flag for value above level                |
| FLAG_BELOW       | Flag for value below level                |
| FORECAST         | Forecast (time linear regression)         |
| INVERT_FLAG      | Invert flag                               |
| KAMA             | Kaufman Adaptive Moving Average (Kaufman) |
| KELTNER          | Keltner Channel                           |
| LATR             | Average True Range (logarithmic)          |
| LOG              | Logarithm                                 |
| MA               | Generic Moving Average                    |
| MACD             | Moving Average Convergenge Divergence     |
| MAD              | Mean Absolute Deviation                   |
| MAX              | Rolling Maximum                           |
| MFI              | Money Flow Index                          |
| MIDPRICE         | Mid Price                                 |
| MIN              | Rolling Minimum                           |
| MINUSDI          | Minus Directional Index                   |
| NATR             | Average True Range (normalized)           |
| PLUSDI           | Plus Directional Index                    |
| PPO              | Price Percentage Oscillator               |
| PRICE            | Generic Price                             |
| RMA              | Rolling Moving Average (RSI Style)        |
| ROC              | Rate of Change                            |
| RSI              | Relative Strength Index                   |
| RVALUE           | RValue (time linear regression)           |
| SAR              | Parabolic Stop and Reverse                |
| SLOPE            | Slope (time linear regression)            |
| SMA              | Simple Moving Average                     |
| STDEV            | Standard Deviation                        |
| STOCH            | Stochastic Oscillator                     |
| STREAK_DOWN      | Consecutive streak of downs               |
| STREAK_UP        | Consecutive streak of ups                 |
| SUM              | Rolling Sum                               |
| TEMA             | Triple Exponential Moving Average         |
| TRANGE           | True Range                                |
| TYPPRICE         | Typical Price                             |
| UPDOWN_FLAG      | Flag for value crossing levels up & down  |
| WCLPRICE         | Weighted Close Price                      |
| WMA              | Weighted Moving Average                   |


