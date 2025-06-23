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

| Name                                               | Description                                      |
|:---------------------------------------------------|:-------------------------------------------------|
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Absolute Value                                   |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Average Directional Index                        |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Arnaud Legoux Moving Average                     |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Average True Range                               |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Average Price                                    |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Bollinger Bands                                  |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Balance of Power                                 |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Commodity Channel Index                          |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Confirmation Lag                                 |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Chaikin Money Flow                               |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Cross Over                                       |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Cross Under                                      |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Curve (quadratic regression)                     |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Double Exponential Moving Average                |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Difference                                       |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Directional Movement Indicator                   |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Exponential Moving Average                       |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Expression Eval (pandas only)                    |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Exponential                                      |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Flag Value                                       |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Hull Moving Average                              |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Kaufman Adaptive Moving Average                  |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Keltner Channel                                  |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Kaufman Efficiency Ratio                         |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Lag Function                                     |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Logarithm                                        |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Logarithmic Rate of Change                       |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Moving Average Convergenge Divergence            |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Rolling Mean Absolute Deviation                  |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Generic Moving Average                           |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Rolling Maximum                                  |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Minus Directional Index                          |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Money Flow Index                                 |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Mid Price                                        |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Rolling Minimum                                  |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Average True Range (normalized)                  |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Plus Directional Index                           |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Price Percentage Oscillator                      |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Generic Price                                    |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Quadratic Series Forecast (quadratic regression) |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Rolling Moving Average (RSI style)               |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Rate of Change                                   |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Relative Strength Index                          |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | R-Value (linear regression)                      |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Parabolic Stop and Reverse                       |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Shift Function                                   |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Sign                                             |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Slope (linear regression)                        |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Simple Moving Average                            |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Standard Deviation                               |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Step Function                                    |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Stochastic Oscillator                            |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Consecutive streak of ups or downs               |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Rolling sum                                      |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Triple Exponential Moving Average                |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | True Range                                       |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Time Series Forecast (linear regression)         |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Typical Price                                    |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Flag for value crossing up & down levels         |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Weighted Close Price                             |
| wrap_indicator.<locals>.decorator.<locals>.wrapper | Weighted Moving Average                          |


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


