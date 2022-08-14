# Minimalist Technical Analysis Library for Python


This library offers a curated list of technical analsysis indicators implemented in cython for improved performance.
The project does not link either numpy, pandas, or any external library,
so the installation should be straightforward.  



> **Warning** This is work in progress. You may want to also look into more mature projects like
[ta-lib](https://pypi.org/project/TA-Lib/).

## Conventions

Price data is expected in the form of a dataframe with
columns ````open, high, low, close, volume````
and a timestamp index called ```date```, all in **lower case**.


## Functions

The submodule ```functions``` offsers a set of functions
named after standard technical analysis indicators in lower caps.
Some functions like ATR require a full price dataframe,
while some simpler function like EMA only requires a single Sseries.  

```python
from mintalib import random_walk

import mintalib.functions as ta

prices = random_walk()

ema50 = ta.sma(prices, 50)
ema200 = ta.sma(prices, 50)
```

## Indicators

The library also offers a set of indicators implemented as classes that bind their parameters and
whose instances can be called as a function.
So for example ```SMA(50)``` is a callable object that will return the 50 period Simple Moving Average of its argument.
Indicators can be chained, like ``<A> | <B>`` meaning that the result of ``<A>`` is used as input to ``<B>``.
Indicators can also be composed, like ``<A> @ <B>`` meaning that ``<A>`` is applied to th result of ``<B>``.
These operators are offered for convenience in composing more complex technical indicators.


<details>
<summary>List of Indicators</summary>


| name              | desc                                   |
|:------------------|:---------------------------------------|
| PRICE             | Price Indicator                        |
| AVGPRICE          | Average Price Indicator                |
| TYPPRICE          | Typical Price Indicator                |
| WCLPRICE          | Weighted Close Price Indicator         |
| MEDPRICE          | Median Price Indicator                 |
| VOLUME            | Volume                                 |
| ROC               | Rate of Change                         |
| DIFF              | Difference                             |
| MIN               | Minimum over a Period                  |
| MAX               | Maximum over a Period                  |
| SUM               | Sum                                    |
| SMA               | Simple Moving Average                  |
| EMA               | Exponential Moving Average             |
| RMA               | Rolling Moving Average (RSI Style)     |
| WMA               | Weighted Moving Average                |
| DEMA              | Double Exponential Moving Average      |
| TEMA              | Triple Exponential Moving Average      |
| RSI               | Relative Streng Index                  |
| ADX               | Average Directional Index              |
| PLUSDI            | PLUS Directional Index                 |
| MINUSDI           | MINUS Directional Index                |
| TRANGE            | True Range                             |
| ATR               | Average True Range                     |
| NATR              | Average True Range (normalized)        |
| LATR              | Average True Range (log prices)        |
| PSAR              | Parabolic Stop and Reverse (cf Wilder) |
| BBANDS            | Bollinger Bands Indicator              |
| KELTNER           | Keltner Bands                          |
| MACD              | Moving Average Convergence Divergence  |
| PPO               | Price Percentage Oscillator            |
| SLOPE             | Slope (Time linear Regression)         |
| SLOPE.CORRELATION | SLope Correlation                      |
| SLOPE.RMSERROR    | Slope Root Mean Square Error           |
| SLOPE.FORECAST    | Slope Forecast                         |
| STDEV             | Standard Deviation                     |
| EVAL              | Expression Eval (pandas only)          |
| TRADE             | Trade Indicator                        |


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
