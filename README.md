# Minimalist Technical Analysis Library for Python


This project aims to offer a curated list of classical technical analysis indicators
implemented in cython for improved performance.
The library does not link numpy, pandas, or any third party binaries,
so the installation should be straightforward.

Most calculations are available either as `functions` or as `indicators`.
Functions and indicators are not interchangeable, and you should select one type or the other
exclusively depending on usage.

The library is compatible with raw `numpy` arrays
as well as `pandas` dataframes and series.
Functions and indicators always wrap their result to match the type of the inputs,
which means that numpy arrays will yield numpy array results
while pandas based inputs will yield pandas based results.
There is experimental support for `polars` dataframes as well. 


> **Warning**
> This is work in progress. For a related project with a mature api you may want to look into
> [ta-lib](https://pypi.org/project/TA-Lib/).


## Conventions

Functions accept either `prices` data or `series` data. Series data can be a numpy array or
a pandas series. Prices data is expected in the form of a dataframe with
columns `open, high, low, close, volume`
and a timestamp index called `date`, all in **lower case**. When working with pure numpy data,
you can represent prices data as a dictionary of numpy arrays with column names a keys,
so as to mimic a dataframe. 


## Functions
Functions can be accessed via the `functions` module. All functions are **upper case**.
It is suggested to import the `functions` module aliased as `ta`.

Some functions like `ATR` require prices data, while other functions like `SMA` work on a single series.
Functions that work on a single series can also be used on prices data and will be applied by default
to the `close` column or the one specified with the `item` parameter.


```python
from mintalib.utils import sample_prices
from mintalib.functions import SMA, MAX, MACD

prices = sample_prices()

sma50 = SMA(prices, 50) # SMA of 'close' with period = 50
vol20 = SMA(prices, 20, item='volume') # SMA of 'volume' with period = 20
high200 = MAX(prices.high, 200) # MAX of 'high' with period = 200. Could also have called with item='high'

macd = MACD(prices) # MACD of 'close'. returns a dataframe with 'macd', 'macdsignal', 'macdhist' columns  
```


<details>
<summary>List of Functions</summary>

| name        | input   | description                                               |
|:------------|:--------|:----------------------------------------------------------|
| AVGPRICE    | prices  | Average Price                                             |
| TYPPRICE    | prices  | Typical Price                                             |
| WCLPRICE    | prices  | Weighted Close Price                                      |
| MIDPRICE    | prices  | Mid Price                                                 |
| PRICE       | prices  | Generic Price                                             |
| CROSSOVER   | series  | 1 when data cross over level, 0.0 elsewhere               |
| CROSSUNDER  | series  | 1 when data cross under level, 0.0 elsewhere              |
| FLAG_ABOVE  | series  | returns flag for strictly positive values                 |
| FLAG_BELOW  | series  | returns flag for strictly negative values                 |
| INVERT_FLAG | series  | returns flag for strictly negative values                 |
| UPDOWN_FLAG | series  | returns flag according to value crossing up & down levels |
| LOG         | series  | Logarithm                                                 |
| EXP         | series  | Exponential                                               |
| ROC         | series  | Rate of Change                                            |
| DIFF        | series  | Difference                                                |
| MIN         | series  | Rolling Minimum                                           |
| MAX         | series  | Rolling Maximum                                           |
| SUM         | series  | Rolling Sum                                               |
| MAD         | series  | Mean Absolute Deviation                                   |
| STDEV       | series  | Standard Deviation                                        |
| SMA         | series  | Simple Moving Average                                     |
| EMA         | series  | Exponential Moving Average                                |
| WMA         | series  | Weighted Moving Average                                   |
| DEMA        | series  | Double Exponential Moving Average                         |
| TEMA        | series  | Triple Exponential Moving Average                         |
| MA          | series  | Generic Moving Average                                    |
| RSI         | series  | Relative Strength Index                                   |
| PLUSDI      | prices  | Plus Directional Index                                    |
| MINUSDI     | prices  | Minus Directional Index                                   |
| ADX         | prices  | Average Directional Index                                 |
| TRANGE      | prices  | True Range                                                |
| ATR         | prices  | Average True Range                                        |
| NATR        | prices  | Average True Range (normalized)                           |
| LATR        | prices  | Average True Range (logarithmic)                          |
| PSAR        | prices  | Parabolic Stop and Reverse                                |
| CCI         | prices  | Commodity Channel Index                                   |
| CMF         | prices  | Chaikin Money Flow                                        |
| MFI         | prices  | Money Flow Index                                          |
| BOP         | prices  | Balance of Power                                          |
| BBANDS      | prices  | Bollinger Bands                                           |
| KELTNER     | prices  | Keltner Channel                                           |
| KAMA        | series  | Kaufman Adaptive Moving Average                           |
| MACD        | series  | Moving Average Convergenge Divergence                     |
| PPO         | series  | Price Percentage Oscillator                               |
| SLOPE       | series  | Slope (time linear regression)                            |
| CURVE       | series  | Curve (time curvilinear regression)                       |
| STOCH       | prices  | Stochastik Oscillator                                     |
| STREAK_UP   | series  | Consecutive streak of ups                                 |
| STREAK_DOWN | series  | Consecutive streak of ups                                 |

</details>

## Indicators

The library also offers a set of indicators. An indicator is a class that be instantiated with its parameters
and whose instance can be called as a function. The same indicator can be reused on multiple different inputs.
So for example `SMA(50)` is a callable object that will return the 50 period simple moving average of its argument.

For convenience an indicator can be applied with the `@` operator without using parentheses.
For example `SMA(50) @ prices` can be used instead of the less readable `SMA(50)(prices)`. 
The same `@` operator can also be used between indicators to mean composition,
where for example `EMA(20) @ ROC(5)` means `EMA(20)` applied to `ROC(5)`.


One way to use indicators is with the pandas assign method,
which allows to add many indicators to a prices dataframe in one go.

```python
from mintalib.indicators import EMA, SMA, ROC, RSI, SLOPE, EVAL

prices = get_prices (...)

prices = prices.assign(
    sma50 = SMA(50),
    sma200 = SMA(200),
    rsi = RSI(14),
    slope = SLOPE(20),
    trend = EMA(20) @ ROC(5),
    pos = EVAL("sma50 > sma200")
)
    
# you will notice that the last EVAL can use any series defined beforehand in the same function call
```

<details>
<summary>List of Indicators</summary>

| name           | description                           |
|:---------------|:--------------------------------------|
| PRICE          | Generic Price                         |
| AVGPRICE       | Average Price Indicator               |
| TYPPRICE       | Typical Price Indicator               |
| WCLPRICE       | Weighted Close Price Indicator        |
| MIDPRICE       | Mid Price Indicator                   |
| VOLUME         | Volume Indicator                      |
| LOG            | Logarithm                             |
| EXP            | Exponential                           |
| ROC            | Rate of Change                        |
| DIFF           | Difference                            |
| MIN            | Rolling Minimum                       |
| MAX            | Rolling Maximum                       |
| SUM            | Rolling Sum                           |
| MAD            | Mean Absolue Deviation                |
| STDEV          | Standard Deviation                    |
| SMA            | Simple Moving Average                 |
| EMA            | Exponential Moving Average            |
| RMA            | Rolling Moving Average (RSI Style)    |
| WMA            | Weighted Moving Average               |
| DEMA           | Double Exponential Moving Average     |
| TEMA           | Triple Exponential Moving Average     |
| RSI            | Relative Streng Index                 |
| ADX            | Average Directional Index             |
| PLUSDI         | Plus Directional Index                |
| MINUSDI        | Minus Directional Index               |
| TRANGE         | True Range                            |
| ATR            | Average True Range                    |
| NATR           | Average True Range (normalized)       |
| LATR           | Average True Range (log prices)       |
| PSAR           | Parabolic Stop and Reverse            |
| CCI            | Commodity Channel Index               |
| CMF            | Chaikin Money Flow                    |
| MFI            | Money Flow Index                      |
| BOP            | Balance of Power                      |
| BBANDS         | Bollinger Bands                       |
| KELTNER        | Keltner Channel                       |
| KAMA           | Kaufman Adaptative Moving Average     |
| MACD           | Moving Average Convergence Divergence |
| PPO            | Price Percentage Oscillator           |
| SLOPE          | Slope (time linear regression)        |
| CURVE          | Curve (time curvilinear regression)   |
| STOCH          | Stockchastic Oscillator               |
| EVAL           | Expression Eval (pandas only)         |
| SLOPE.RVALUE   | Slope R-Value                         |
| SLOPE.ERROR    | Slope Root Mean Square Error          |
| SLOPE.FORECAST | Slope Forecast                        |
| CURVE.RVALUE   | Curve R-Value                         |
| CURVE.ERROR    | Curve Root Mean Square Error          |

</details>

## Examples

You can find example notebooks in the [examples](/examples/) folder. 


## Developer Notes


You can install the current version of this package with pip
```console
python3 -mpip install git+ssh://git@github.com/furechan/mintalib.git
```

Or to install from a local copy
```console
pip install <folder>
```
