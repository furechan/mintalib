# Minimal Technical Analysis Library for Python

This package offers a curated list of technical analysis indicators implemented in `cython` for optimal performance. The library is built around `numpy` arrays and offers a variety interface for `pandas` and `polars` dataframes and series.

> **Warning** This project is experimental and the interface is likely to change.


## Functions

Concrete calculation functions are available from the `mintalib.function` module with names like `sma`, `atr`, `macd`, etc.

The first parameter of a function is either `prices` or `series` depending on whether
the function expects a dataframe of prices or a single series.

A `prices` dataframe can be a pandas or polars dataframe. The column names for prices are expected to include `open`, `high`, `low`, `close`, `volume` all in **lower case**.

A `series` can be a pandas/polars series or a numpy array.

```python
import mintalib.functions as ta

prices = ... # pandas/polars DataFrame

sma = ta.sma(prices, 50)
atr = ta.atr(prices, 14)
```

# Pandas Extension

Mintalib can be used as a pandas extension via a `ts` accessor. Series calculations are accessible on pandas series, and prices calculations are accessible on dataframes.

To activate the extension you only need to import the module `mintalib.pandas`.

```python
import mintalib.pandas # noqa F401

prices = ... # pandas DataFrame

sma = prices.close.ts.sma(50)
atr = prices.ts.atr(14)
```

# Polars Expressions

Mintalib offers expression factory methods via the `mintalib.expressions` module.
The methods accept a source expression through the keyword-only `src` parameter.
The source expression can also be passed as the first parameter to facilitate the use with `pipe`.


```python
import mintalib.expressions as ta

prices = ... # polars DataFrame

prices.select(
    ta.macd().struct.unnest(),
    sma=ta.sma(50),
    atr=ta.atr(14),
    trend=ta.ema(50).pipe(ta.roc, 1)
)
```

# Polars Extension

Mintalib can be used as a polars extension via a `ts` accessor for polars series, dataframes and expressions. 
Indicators that expect a prices inputs should be invoked on a struct with all required fields (see `OHLC` in example below). Indicators with multi column outputs like `macd` return a polars struct.

To activate the extension you only need to import the module `mintalib.polars`.


```python
from mintalib.polars import CLOSE, OHLC

# CLOSE is short-hand for pl.col('close')
# OHLC is short-hand for pl.struct(['open', 'high', 'low', 'close'])

prices = ... # polars DataFrame

prices.select(
    CLOSE.ts.macd().struct.unnest(),
    sma=CLOSE.ts.sma(50),
    atr=OHLC.ts.atr(),
    trend=CLOSE.ts.ema(20).ts.roc(1)
)
```


## Using Indicators (Legacy Interface)

Indicators offer a composable interface where a calculation function is bound with its parameters into a callable object. Indicators are accessible from the `mintalib.indicators` module with names like `EMA`, `SMA`, `ATR`, `MACD`, etc ... 

An indicator instance can be invoked as a function or via the `@` operator as syntactic sugar. 

So for example `SMA(50) @ prices` can be used to compute the 50 period simple moving average on `prices`, in place of `SMA(50)(prices)`. 

The `@` operator can also be used to chain indicators, where for example `ROC(1) @ EMA(20)` means `ROC(1)` applied to `EMA(20)`.

```python
from mintalib.indicators import SMA, EMA, ROC, MACD

prices = ... # pandas DataFrame

result = prices.assign(
    sma50 = SMA(50),
    sma200 = SMA(200),
    rsi = RSI(14),
    trend = ROC(1) @ EMA(20)
)
```



## List of Indicators

| Name       | Description                                                   |
|:-----------|:--------------------------------------------------------------|
| ABS        | Absolute Value                                                |
| ADX        | Average Directional Index                                     |
| ALMA       | Arnaud Legoux Moving Average                                  |
| ATR        | Average True Range                                            |
| AVGPRICE   | Average Price                                                 |
| BBANDS     | Bollinger Bands                                               |
| BBP        | Bollinger Bands Percent (%B)                                  |
| BBW        | Bollinger Bands Width                                         |
| BOP        | Balance of Power                                              |
| CCI        | Commodity Channel Index                                       |
| CLAG       | Confirmation Lag                                              |
| CMF        | Chaikin Money Flow                                            |
| CROSSOVER  | Cross Over                                                    |
| CROSSUNDER | Cross Under                                                   |
| CURVE      | Curve (quadratic regression)                                  |
| DEMA       | Double Exponential Moving Average                             |
| DIFF       | Difference                                                    |
| DMI        | Directional Movement Indicator                                |
| EMA        | Exponential Moving Average                                    |
| EVAL       | Expression Eval (pandas only)                                 |
| EXP        | Exponential                                                   |
| FLAG       | Flag Value                                                    |
| HMA        | Hull Moving Average                                           |
| KAMA       | Kaufman Adaptive Moving Average                               |
| KELTNER    | Keltner Channel                                               |
| KER        | Kaufman Efficiency Ratio                                      |
| LAG        | Lag Function                                                  |
| LOG        | Logarithm                                                     |
| LROC       | Logarithmic Rate of Change                                    |
| MACD       | Moving Average Convergenge Divergence                         |
| MACDV      | Moving Average Convergenge Divergence - Volatility Normalized |
| MAD        | Rolling Mean Absolute Deviation                               |
| MAV        | Generic Moving Average                                        |
| MAX        | Rolling Maximum                                               |
| MDI        | Minus Directional Index                                       |
| MFI        | Money Flow Index                                              |
| MIDPRICE   | Mid Price                                                     |
| MIN        | Rolling Minimum                                               |
| NATR       | Average True Range (normalized)                               |
| PDI        | Plus Directional Index                                        |
| PPO        | Price Percentage Oscillator                                   |
| PRICE      | Generic Price                                                 |
| QSF        | Quadratic Series Forecast (quadratic regression)              |
| RMA        | Rolling Moving Average (RSI style)                            |
| ROC        | Rate of Change                                                |
| RSI        | Relative Strength Index                                       |
| RVALUE     | R-Value (linear regression)                                   |
| SAR        | Parabolic Stop and Reverse                                    |
| SHIFT      | Shift Function                                                |
| SIGN       | Sign                                                          |
| SLOPE      | Slope (linear regression)                                     |
| SMA        | Simple Moving Average                                         |
| STDEV      | Standard Deviation                                            |
| STEP       | Step Function                                                 |
| STOCH      | Stochastic Oscillator                                         |
| STREAK     | Consecutive streak of values above zero                       |
| SUM        | Rolling sum                                                   |
| TEMA       | Triple Exponential Moving Average                             |
| TRANGE     | True Range                                                    |
| TSF        | Time Series Forecast (linear regression)                      |
| TYPPRICE   | Typical Price                                                 |
| UPDOWN     | Flag for value crossing up & down levels                      |
| WCLPRICE   | Weighted Close Price                                          |
| WMA        | Weighted Moving Average                                       |


## Example Notebooks

Example notebooks in the `examples` folder. 


## Installation

You can install this package with pip

```console
pip install mintalib
```

## Dependencies

- python >= 3.10
- numpy
- pandas
- polars [optional]


## Related Projects

- [ta-lib](https://github.com/mrjbq7/ta-lib) Python wrapper for TA-Lib
- [qtalib](https://github.com/josephchenhk/qtalib) Quantitative Technical Analysis Library
- [polars-ta](https://github.com/wukan1986/polars_ta) Technical Analysis Indicators for polars
- [polars-talib](https://github.com/Yvictor/polars_ta_extension) Polars extension for Ta-Lib: Support Ta-Lib functions in Polars expressions


