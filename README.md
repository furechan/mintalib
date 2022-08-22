# Minimalist Technical Analysis Library for Python


This project aims at offering a curated list of classical technical analsysis indicators
implemented in cython for improved performance.
The library does not link numpy, pandas, or any third party binaries,
so the installation should be straightforward.


> **Warning**
> This is work in progress. For a related project with a mature api you may want to look into
> [ta-lib](https://pypi.org/project/TA-Lib/).


## Conventions

Functions and indicators accept either series data or prices data. Series data can be a numpy array or
a pandas series. Prices data is expected in the form of a dataframe with
columns typically `open, high, low, close, volume`
and a timestamp index called `date`, all in **lower case**. When working with pure numpy data,
you can also represent prices data as a dictionary of arrays with column names a keys,
so as to mimic a dataframe.  


## Functions
Functions can be accessed via the `functions` module. All functions are **lower case**.
It is suggested to import the `functions` module aliased as `ta`.

Some functions like `atr` require prices data, while other functions like `sma` work on a single series.
Series based functions when called with a prices dataframe
will be applied by default to the `close` column or the column specified with the `item` parameter.


Most functions return data in the same form as the data input.
If called with a numpy array they will return a numpy array (or tuple of such).
If called with a pandas object they will return a pandas object with the same index. 

```python
import mintalib.functions as ta

from mintalib.utils import sample_prices

prices = sample_prices()

sma50 = ta.sma(prices, 50) # SMA of 'close' with period = 50
vol20 = ta.sma(prices, 20, item='volume') # SMA of 'volume' with period = 20
high200 = ta.max(prices.high, 200) # MAX of 'high' with period = 200. Could also have called with item='high'

macd = ta.macd(prices) # MACD of 'close'. returns a dataframe with 'macd', 'macdsignal', 'macdhist' columns  

```


<details>
<summary>List of Functions</summary>

| name     | input   | description                           |
|:---------|:--------|:--------------------------------------|
| avgprice | prices  | Average Price                         |
| typprice | prices  | Typical Price                         |
| wclprice | prices  | Weighted Close Price                  |
| midprice | prices  | Mid Price                             |
| log      | series  | Logarithm                             |
| exp      | series  | Exponential                           |
| roc      | series  | Rate of Change                        |
| diff     | series  | Difference                            |
| min      | series  | Rolling Minimum                       |
| max      | series  | Rolling Maximum                       |
| sum      | series  | Rolling Sum                           |
| mad      | series  | Mean Absolute Deviation               |
| stdev    | series  | Standard Deviation                    |
| sma      | series  | Simple Moving Average                 |
| ema      | series  | Exponential Moving Average            |
| rma      | series  | Rolling Moving Average (RSI Style)    |
| wma      | series  | Weighted Moving Average               |
| dema     | series  | Double Exponential Moving Average     |
| tema     | series  | Triple Exponential Moving Average     |
| ma       | series  | Generic Moving Average                |
| rsi      | series  | Relative Strength Index               |
| plusdi   | prices  | Plus Directional Index                |
| minusdi  | prices  | Minus Directional Index               |
| adx      | prices  | Average Directional Index             |
| trange   | prices  | True Range                            |
| atr      | prices  | Average True Range                    |
| natr     | prices  | Average True Range (normalized)       |
| latr     | prices  | Average True Range (logarithmic)      |
| psar     | prices  | Parabolic Stop and Reverse            |
| cci      | prices  | Commodity Channel Index               |
| cmf      | prices  | Chaikin Money Flow                    |
| mfi      | prices  | Money Flow Index                      |
| bop      | prices  | Balance of Power                      |
| bbands   | prices  | Bollinger Bands                       |
| keltner  | prices  | Keltner Channel                       |
| macd     | series  | Moving Average Convergenge Divergence |
| ppo      | series  | Price Percentage Oscillator           |
| slope    | series  | Slope (time linear regression)        |
| curve    | series  | Curve (time curvilinear regression)   |
| stoch    | prices  | Stochastik Oscillator                 |
| streak   | series  | Consecutive streak of ups/downs       |

</details>

## Indicators

The library also offers a set of indicators. An indicator is a class that be be instantiated with its parameters
and whose instance can be called as a function. An indicator can then be reused on multiple different inputs.
So for example `SMA(50)` is a callable object that will return the 50 period simple moving average of its argument.

One neat way to use indicators is with the pandas assign method, so as to apply multiple indicators in one go. For example:

```python
from mintalib.indicators import SMA, RSI, SLOPE, EVAL

prices = get_prices (...)

prices = prices.assign(
    sma50 = SMA(50),
    sma200 = SMA(200),
    rsi = RSI(14),
    slope = SLOPE(20),
    pos = EVAL("sma50 > sma200')
)
    
# you will notice that the last EVAL can use series defined right above in the same function call
```

For syntactic convenience an indicator can be applied with the `@` operator so as to avoid the collision of parentheses.
For example `SMA(50) @ prices` can be used instead of the less readable `SMA(50)(prices)`. 
The same `@` operator can also be used between indicators to mean composition.
Where for example `EMA(20) @ ROC(5)` means `EMA(20)` applied to `ROC(5)`.


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
| MACD           | Moving Average Convergence Divergence |
| PPO            | Price Percentage Oscillator           |
| SLOPE          | Slope (time linear regression)        |
| SLOPE.RVALUE   | Slope R-Value (Correlation)           |
| SLOPE.ERROR    | Slope Root Mean Square Error          |
| SLOPE.FORECAST | Slope Forecast                        |
| CURVE          | Curve (time curvilinear regression)   |
| CURVE.RVALUE   | Curve R-Value                         |
| CURVE.ERROR    | Curve Root Mean Square Error          |
| STOCH          | Stockchastic Oscillator               |
| EVAL           | Expression Eval (pandas only)         |

</details>

## Developer Notes


To compile the extension:
```console
python setup.py build_ext --inplace
```

To install the extension:
```console
pip install <folder>
```

To develop the extension (either):
```console
python setup.py develop
```
```console
pip install -e <folder>
```
