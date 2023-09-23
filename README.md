# Minimal Technical Analysis Library for Python


This library offers a short list of technical analysis indicators
implemented in cython for improved performance.

It is built around `numpy` arrays and aims to be compatible
with `pandas` and `polars` where possible.

The core extension is not dependent on `pandas`
but some helper modules like `reflib` and `utils` are.


> **Note**
> This is work in progress.
> For a similar project with a mature api
> you may want to look at [ta-lib](https://pypi.org/project/TA-Lib/).


## Conventions

Indicators accept either `series` or `prices` data.
`series` data must be compatible with one dimensional numpy arrays.
`prices` data is expected in the form of a dataframe
with columns `open`, `high`, `low`, `close`, `volume` all in **lower case**.
For `prices`, instead of a standard dataframe
you can also use a numpy structured array or equivelent structure
that offers dictionary based access to it columns.   



## Functions

Indicators are available as functions that can be accessed via the `core` module.
All function names like `EMA`, `SMA`, `ROC`, `MACD`, ... are **upper case**.

Some functions like `ATR` require `prices` data, while other functions like `SMA` work on a `series`.
Functions that work on a single series can also be used on prices data and will be applied 
to the `close` column by default or otherwize the one specified with the `item` parameter.

Most functions automatically wrap their result to match their input, so that for example 
pandas based inputs will yield pandas based results with a matching datetime index.

```python
from mintalib.core import SMA, MAX
from mintalib.samples import sample_prices

prices = sample_prices()

sma50 = SMA(prices, 50)  # SMA of 'close' with period = 50
sma200 = SMA(prices, 200)  # SMA of 'close' with period = 50
high200 = MAX(prices, 200, item='high')  # MAX of 'high' with period = 200

```

## Operands

Indicators are also available as operands that can be accessed via the `opers` module.

An operand is an indicator with all parameters specifed at creation.
Operands are callable object and can be invoked as a regular function.

So for example `SMA(50)` is a callable object that will return the 50 period simple moving average of its argument.

Operands can also be applied to prices with the `@` operator.

For example `SMA(50) @ prices` can be used to compute the 50 period simple moving average on prices. 

Operands can also be composed with the `@` operator.

Where for example `EMA(20) @ ROC(5)` means `EMA(20)` applied to `ROC(5)`.

When using pandas you can apply multiple operands in one single calculation with the `assign` method.

```python
from mintalib.opers import EMA, SMA, ROC, RSI, SLOPE, EVAL
from mintalib.samples import sample_prices

prices = sample_prices(target='pandas')

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
python -mpip install git+ssh://git@github.com/furechan/mintalib.git
```

## List of Functions

| Name             | Input   | Description                                               |
|:-----------------|:--------|:----------------------------------------------------------|
| AVGPRICE         | prices  | Average Price                                             |
| TYPPRICE         | prices  | Typical Price                                             |
| WCLPRICE         | prices  | Weighted Close Price                                      |
| MIDPRICE         | prices  | Mid Price                                                 |
| PRICE            | prices  | Generic Price                                             |
| CROSSOVER        | series  | 1 when data cross over level, 0.0 elsewhere               |
| CROSSUNDER       | series  | 1 when data cross under level, 0.0 elsewhere              |
| FLAG_ABOVE       | series  | returns flag for strictly positive values                 |
| FLAG_BELOW       | series  | returns flag for strictly negative values                 |
| INVERT_FLAG      | series  | returns flag for strictly negative values                 |
| UPDOWN_FLAG      | series  | returns flag according to value crossing up & down levels |
| LOG              | series  | Logarithm                                                 |
| EXP              | series  | Exponential                                               |
| ROC              | series  | Rate of Change                                            |
| DIFF             | series  | Difference                                                |
| MIN              | series  | Rolling Minimum                                           |
| MAX              | series  | Rolling Maximum                                           |
| SUM              | series  | Rolling Sum                                               |
| MAD              | series  | Mean Absolute Deviation                                   |
| STDEV            | series  | Standard Deviation                                        |
| SMA              | series  | Simple Moving Average                                     |
| EMA              | series  | Exponential Moving Average                                |
| RMA              | series  | Rolling Moving Average (RSI Style)                        |
| WMA              | series  | Weighted Moving Average                                   |
| DEMA             | series  | Double Exponential Moving Average                         |
| TEMA             | series  | Triple Exponential Moving Average                         |
| MA               | series  | Generic Moving Average                                    |
| RSI              | series  | Relative Strength Index                                   |
| PLUSDI           | prices  | Plus Directional Index                                    |
| MINUSDI          | prices  | Minus Directional Index                                   |
| ADX              | prices  | Average Directional Index                                 |
| TRANGE           | prices  | True Range                                                |
| ATR              | prices  | Average True Range                                        |
| NATR             | prices  | Average True Range (normalized)                           |
| LATR             | prices  | Average True Range (logarithmic)                          |
| PSAR             | prices  | Parabolic Stop and Reverse                                |
| CCI              | prices  | Commodity Channel Index                                   |
| CMF              | prices  | Chaikin Money Flow                                        |
| MFI              | prices  | Money Flow Index                                          |
| BOP              | prices  | Balance of Power                                          |
| BBANDS           | prices  | Bollinger Bands                                           |
| KELTNER          | prices  | Keltner Channel                                           |
| EFFICIENCY_RATIO | series  | Efficiency Ratio                                          |
| KAMA             | series  | Kaufman Adaptive Moving Average                           |
| MACD             | series  | Moving Average Convergenge Divergence                     |
| PPO              | series  | Price Percentage Oscillator                               |
| SLOPE            | series  | Slope (time linear regression)                            |
| CURVE            | series  | Curve (time curvilinear regression)                       |
| STOCH            | prices  | Stochastik Oscillator                                     |
| STREAK_UP        | series  | Consecutive streak of ups                                 |
| STREAK_DOWN      | series  | Consecutive streak of ups                                 |
| EVAL             | prices  | Expression Eval (pandas only)                             |
