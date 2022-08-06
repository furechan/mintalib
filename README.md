# Minimalist Technical Analysis Library for Python


## Warning

This project is for experimentation only. Anything can change and some things have not been thoroughly tested. For any serious usage I recommend you look at 
the [talib](https://pypi.org/project/TA-Lib/) library.

## Purpose

This library offers a curated list of technical analsysis indicators,
some of which are implemented in cython for improved performance.
The runtime dependencies are limited to numpy and pandas.


## Conventions

Price data is expected in the form of a pandas DataFrames with
columns ````open, high, low, close, volume````
and a timestamp index called ```date```.  

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
