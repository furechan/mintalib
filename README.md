# Minimalist Technical Analysis Library for Python


## Warning

This project is experimental. For any serious usage you may want to look into 
the [ta-lib](https://pypi.org/project/TA-Lib/) library.

## Purpose

This library offers a curated list of technical analsysis indicators.
Most of the library is implemented in cython to offer improved performance.
The project does not link numpy or pandas binaries, or any external library,
so the installation should be straightforward.  

## Conventions

Price data is expected in the form of a pandas DataFrames with
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
