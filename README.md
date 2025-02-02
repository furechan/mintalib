# Minimal Technical Analysis Library for Python

This package offers a curated list of technical analysis indicators and timeseries calculations
all implemented in cython for improved performance. The library is built around `numpy` arrays,
and is compatible with `pandas` dataframes and series.


> **Warning**
> This project is experimental and the interface can change.
> For a similar project with a mature api you may want to look into
> [ta-lib](https://pypi.org/project/TA-Lib/).


## Structure

The `mintalib` package contains three main modules:

- [mintalib.core](/docs/mintalib.core.md)
    core calculation rountines implemented in cython, with names like `calc_sma`, `calc_ema`, etc ...  
- [mintalib.functions](/docs/mintalib.functions.md)
    wrapper functions to compute calculations on series and dataframes, with names like `sma`, `ema`, etc ...
- [mintalib.indicators](/docs/mintalib.indicators.md)
    composable interface to indicators with names like `SMA`, `EMA`, etc ...


## List of Indicators

| Name       | Description                              |
|:-----------|:-----------------------------------------|
| ABS        | Absolute Value                           |
| ADX        | Average Directional Index                |
| ALMA       | Arnaud Legoux Moving Average             |
| ATR        | Average True Range                       |
| AVGPRICE   | Average Price                            |
| BBANDS     | Bollinger Bands                          |
| BOP        | Balance of Power                         |
| CCI        | Commodity Channel Index                  |
| CLAG       | Confirmation Lag                         |
| CMF        | Chaikin Money Flow                       |
| CROSSOVER  | Cross Over                               |
| CROSSUNDER | Cross Under                              |
| CURVE      | Curve (quadratic regression)             |
| DEMA       | Double Exponential Moving Average        |
| DIFF       | Difference                               |
| DMI        | Directional Movement Indicator           |
| EMA        | Exponential Moving Average               |
| EVAL       | Expression Eval (pandas only)            |
| EXP        | Exponential                              |
| FLAG       | Flag Value                               |
| HMA        | Hull Moving Average                      |
| KAMA       | Kaufman Adaptive Moving Average          |
| KELTNER    | Keltner Channel                          |
| KER        | Kaufman Efficiency Ratio                 |
| LAG        | Lag Function                             |
| LOG        | Logarithm                                |
| LROC       | Logarithmic Rate of Change               |
| MACD       | Moving Average Convergenge Divergence    |
| MAD        | Rolling Mean Absolute Deviation          |
| MAV        | Generic Moving Average                   |
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
| RVALUE     | R-Value (linear regression)              |
| SAR        | Parabolic Stop and Reverse               |
| SHIFT      | Shift Function                           |
| SIGN       | Sign                                     |
| SLOPE      | Slope (linear regression)                |
| SMA        | Simple Moving Average                    |
| STDEV      | Standard Deviation                       |
| STEP       | Step Function                            |
| STOCH      | Stochastic Oscillator                    |
| STREAK     | Consecutive streak of ups or downs       |
| SUM        | Rolling sum                              |
| TEMA       | Triple Exponential Moving Average        |
| TRANGE     | True Range                               |
| TSF        | Time Series Forecast (linear regression) |
| TYPPRICE   | Typical Price                            |
| UPDOWN     | Flag for value crossing up & down levels |
| WCLPRICE   | Weighted Close Price                     |
| WMA        | Weighted Moving Average                  |


## Using Functions

Functions are available as lower case methods like `sma`, `ema`, etc ...
The best way to use this module is to alias it to a short name
like `ta` and access all functions as attributes.

```python
import mintalib.functions as ta
```

The first parameter of a function is either `prices` or `series` depending on whether
the functions expects a dataframe of prices or a single series.

Functions that expect series data can be applied to a prices dataframe, in which case they use 
the column specified with the `item` parameter or by default the 'close' column.

A `prices` dataframe can be a pandas dataframe or a dictionary of numpy arrays.
The column names for prices are expected to include `open`, `high`, `low`, `close`, `volume` all in **lower case**.

A `series` can be a pandas series or any iterable compatible with numpy arrays.

Functions automatically wrap the result to match the type and the index of the input data when applicable.


```python
import yfinance as yf
import mintalib.functions as ta

# fetch prices (eg with yfinance)
prices = yf.Ticker('AAPL').history('5y')

# convert column and index names to lower case
prices = prices.rename(columns=str.lower).rename_axis(index=str.lower)

# compute indicators
sma50 = ta.sma(prices, 50)  # SMA of 'close' with period 50
sma200 = ta.sma(prices, 200)  # SMA of 'close' with period 200
high200 = ta.max(prices, 200, item='high')  # MAX of 'high' with period 200
```


## Using Indicators

Indicators are available via the `indicators` module, with similar names as functions but in **upper case**.

Indicators offer a composable interface where a function is bound with its calculation parameters. When instantiated with parameters an indicator yields a callable that can be applied to prices or series data.

An indicator is a callable that accepts a series or a prices dataframe as a single parameter. You can also use the `@` operator as syntactic sugar to apply an indicator to its parameter. 

So for example `SMA(50) @ prices` can be used to compute the 50 period simple moving average on `prices`, instead of the more verbose `SMA(50)(prices)`. 

```python
from mintalib.indicators import ROC, SMA, EMA

sma50 = SMA(50) @ prices    # SMA of 'close' with period 50
sma200 = SMA(200) @ prices  # SMA of 'close' with period 200
high200 = MAX(200, item='high') @ prices    # MAX of 'high' with period 200
```


The `@` operator can also be used to chain indicators, where for example `ROC(1) @ EMA(20)` means `ROC(1)` applied to `EMA(20)`.


```python
from mintalib.indicators import ROC, SMA, EMA

trend = ROC(1) @ EMA(20) @ prices
```


With pandas dataframes you can compose and apply multiple indicators in one call using the `assign` dataframe method.

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
    trend = ROC(1) @ EMA(20),
    flag = EVAL("sma50 > sma200")
)
```


## Example Notebooks

You can find example notebooks in the `examples` folder. 


## Installation

You can install this package with pip

```console
pip install mintalib
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
- [yfinance](https://github.com/ranaroussi/yfinance) Download market data from Yahoo! Finance's API


