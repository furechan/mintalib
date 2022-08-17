# Minimalist Technical Analysis Library for Python


This project offers a curated list of technical analsysis indicators implemented in cython for improved performance.
The compilation does not link numpy, pandas, or any external libraries,
so the installation should be straightforward.  


> **Warning** This is work in progress. For a related project with a mature api you may want to look into
> [ta-lib](https://pypi.org/project/TA-Lib/).

## Conventions

Price data is expected in the form of a dataframe with
columns ````open, high, low, close, volume````
and a timestamp index called ```date```, all in **lower case**.


## Functions

The submodule ```functions``` offsers a set of functions
named after standard technical analysis indicators, all in lower caps.
Some functions like `atr` require a price dataframe,
while some simpler function like `ema` only require a series.  

```python
import mintalib.functions as ta

from mintalib.utils import random_walk

series = random_walk()

ema50 = ta.sma(series, 50)
ema200 = ta.sma(series, 50)
```


<details>
<summary>List of Functions</summary>

| name     | description                           |
|:---------|:--------------------------------------|
| avgprice | Average Price                         |
| typprice | Typical Price                         |
| wclprice | Weighted Close Price                  |
| midprice | Mid Price                             |
| roc      | Rate of Change                        |
| diff     | Difference                            |
| min      | Rolling Minimum                       |
| max      | Rolling Maximum                       |
| sum      | Rolling Sum                           |
| sma      | Simple Moving Average                 |
| ema      | Exponential Moving Average            |
| rma      | Rolling Moving Average (RSI Style)    |
| wma      | Weighted Moving Average               |
| dema     | Double Exponential Moving Average     |
| tema     | Triple Exponential Moving Average     |
| ma       | Generic Moving Average                |
| rsi      | Relative Strength Index               |
| plusdi   | Plus Directional Index                |
| minusdi  | Minus Directional Index               |
| adx      | Average Directional Index             |
| trange   | True Range                            |
| atr      | Average True Range                    |
| natr     | Normalized Average True Range         |
| latr     | Normalized Average True Range         |
| psar     | Parabolic Stop and Reverse            |
| bbands   | Bollinger Bands                       |
| keltner  | Keltner Bands                         |
| macd     | Moving Average Convergenge Divergence |
| ppo      | Price Percentage Oscillator           |
| slope    | Slope (time linear regression)        |
| curve    | Curve (time curvilinear regression)   |
| stdev    | Standard Deviation                    |
| stoch    | Stochastik Oscillator                 |
| streak   | streak                                |

</details>

## Indicators

The library also offers a set of indicators implemented as classes that bind their parameters and
whose instances can be called as a function.
So for example ```SMA(50)``` is a callable object that will return the 50 period Simple Moving Average of its argument.
Indicators can be chained, like ``<A> | <B>`` meaning that the result of ``<A>`` is used as input to ``<B>``.
Indicators can also be composed, like ``<A> @ <B>`` meaning that ``<A>`` is applied to th result of ``<B>``.
These operators are offered for convenience in composing more complex technical indicators.


<details>
<summary>List of Indicators</summary>

| name     | description                           |
|:---------|:--------------------------------------|
| PRICE    | Price Indicator                       |
| AVGPRICE | Average Price Indicator               |
| TYPPRICE | Typical Price Indicator               |
| WCLPRICE | Weighted Close Price Indicator        |
| MIDPRICE | Mid Price Indicator                   |
| VOLUME   | Volume Indicator                      |
| ROC      | Rate of Change                        |
| DIFF     | Difference                            |
| MIN      | Rolling Minimum                       |
| MAX      | Rolling Maximum                       |
| SUM      | Rolling Sum                           |
| SMA      | Simple Moving Average                 |
| EMA      | Exponential Moving Average            |
| RMA      | Rolling Moving Average (RSI Style)    |
| WMA      | Weighted Moving Average               |
| DEMA     | Double Exponential Moving Average     |
| TEMA     | Triple Exponential Moving Average     |
| RSI      | Relative Streng Index                 |
| ADX      | Average Directional Index             |
| PLUSDI   | Plus Directional Index                |
| MINUSDI  | Minus Directional Index               |
| TRANGE   | True Range                            |
| ATR      | Average True Range                    |
| NATR     | Average True Range (normalized)       |
| LATR     | Average True Range (log prices)       |
| PSAR     | Parabolic Stop and Reverse            |
| BBANDS   | Bollinger Bands                       |
| KELTNER  | Keltner Bands                         |
| MACD     | Moving Average Convergence Divergence |
| PPO      | Price Percentage Oscillator           |
| SLOPE    | Slope (time linear Regression)        |
| CURVE    | Curve (time curvilinear regression)   |
| STDEV    | Standard Deviation                    |
| STOCH    | Stockchastic Oscillator               |
| EVAL     | Expression Eval (pandas only)         |

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
