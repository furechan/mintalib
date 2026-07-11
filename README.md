# Minimal Technical Analysis Library for Python

This package offers a curated list of technical analysis indicators implemented in `Cython` for optimal performance. The library is built around `numpy` arrays and offers a variety of interfaces for `pandas` and `polars` dataframes and series.

> [!WARNING]
> This project is experimental and the interface is likely to change.


## Installation

Pick the backend you want to use — pandas and polars are both optional extras:

```console
pip install mintalib[pandas]          # pandas DataFrames
pip install mintalib[polars]          # polars DataFrames
pip install mintalib[pandas,polars]   # both
```

A bare `pip install mintalib` installs only numpy (the core computation layer).

## Dependencies

- python >= 3.10
- numpy
- pandas [optional]
- polars [optional]


## Interfaces

Mintalib provides three interfaces for different workflows:

- **Functions** (`mintalib.functions`) — plain functions, useful for scripting or building custom pipelines (work with both pandas and polars)
- **Polars Expressions** (`mintalib.expressions`) — composable polars expressions, best for polars-native workflows
- **Indicators** (`mintalib.indicators`) — callable objects that bind a calculation with its parameters; **pandas only**


## Functions

Calculation functions are available from the `mintalib.functions` module with names in lower case like `sma`, `atr`, `macd`, etc.

Functions are polyvalent. They can be applied equaly to pandas or polars dataframes and series.

The first parameter of a function is either `prices` or `series` depending on whether
the function expects a dataframe of prices or a single series.

A `prices` dataframe can be a pandas or polars dataframe. The column names for prices are expected to include `open`, `high`, `low`, `close`, `volume` all in **lower case**.

A `series` can be a pandas/polars series or a numpy array.

```python
import mintalib.functions as ta

prices = ... # pandas/polars DataFrame

sma = ta.sma(prices['close'], 50)
atr = ta.atr(prices, 14)
```


## Expressions

Mintalib offers expression factory methods via the `mintalib.expressions` module with names in upper case like `EMA`, `SMA`, `ATR`, `MACD`, ...
The methods accept a source expression as an optional keyword-only `src` parameter.
The source expression can also be passed as the first parameter to facilitate the use with `pipe`, e.g. `EMA(20).pipe(ROC, 1)` applies `ROC(1)` on top of `EMA(20)`. Multi-column calculations like `MACD` return a polars struct expression.

When no source is given, series-based expressions (e.g. `EMA`, `SMA`) default to the `close` column, while prices-based ones (e.g. `ATR`, `MACD`) read the full DataFrame.

```python
from mintalib.expressions import EMA, SMA, ATR, ROC, MACD

prices = ... # polars DataFrame

prices.with_columns(
    ema=EMA(20),
    atr=ATR(14),
    trend=EMA(20).pipe(ROC, 1)   # ROC(1) applied to EMA(20)
)
```

## Indicators

Indicators offer a composable interface where a calculation function is bound with its parameters into a callable object. Indicators are accessible from the `mintalib.indicators` module with names in upper case like `EMA`, `SMA`, `ATR`, `MACD`, etc ...

Indicators work only on pandas DataFrames and Series.

An indicator instance is callable: `SMA(50)(prices)` applies it to data. The pandas idiom `prices.pipe(SMA(50))` works equivalently.

Indicators chain with `|`, where for example `EMA(20) | ROC(1)` means `ROC(1)` applied after `EMA(20)`. The `.then()` method is the fluent equivalent.

```python
from mintalib.indicators import SMA, EMA, ROC, RSI, MACD

prices = ... # pandas DataFrame

result = prices.assign(
    ema20 = EMA(20),
    rsi = RSI(14),
    trend = EMA(20) | ROC(1)
)
```

## List of Indicators

| Name       | Input   | Description                                                   |
|:-----------|:--------|:--------------------------------------------------------------|
| ABS        | Series  | Absolute Value                                                |
| ADX        | Prices  | Average Directional Index                                     |
| ALMA       | Series  | Arnaud Legoux Moving Average                                  |
| ATR        | Prices  | Average True Range                                            |
| AVGPRICE   | Prices  | Average Price                                                 |
| BBANDS     | Prices  | Bollinger Bands                                               |
| BBP        | Prices  | Bollinger Bands Percent (%B)                                  |
| BBW        | Prices  | Bollinger Bands Width                                         |
| BOP        | Prices  | Balance of Power                                              |
| CCI        | Prices  | Commodity Channel Index                                       |
| CLAG       | Series  | Confirmation Lag                                              |
| CMF        | Prices  | Chaikin Money Flow                                            |
| CROSSOVER  | Series  | Cross Over                                                    |
| CROSSUNDER | Series  | Cross Under                                                   |
| CURVE      | Series  | Curve (quadratic regression)                                  |
| DEMA       | Series  | Double Exponential Moving Average                             |
| DIFF       | Series  | Difference                                                    |
| DMI        | Prices  | Directional Movement Indicator                                |
| DONCHIAN   | Prices  | Donchian Channel                                              |
| EMA        | Series  | Exponential Moving Average                                    |
| EVAL       | Prices  | Evaluate a pandas expression against a DataFrame's columns.   |
| EXP        | Series  | Exponential                                                   |
| FLAG       | Series  | Flag Value                                                    |
| HMA        | Series  | Hull Moving Average                                           |
| KAMA       | Series  | Kaufman Adaptive Moving Average                               |
| KELTNER    | Prices  | Keltner Channel                                               |
| KER        | Series  | Kaufman Efficiency Ratio                                      |
| LAG        | Series  | Lag Function                                                  |
| LOG        | Series  | Logarithm                                                     |
| LROC       | Series  | Logarithmic Rate of Change                                    |
| MACD       | Series  | Moving Average Convergence Divergence                         |
| MACDV      | Prices  | Moving Average Convergence Divergence - Volatility Normalized |
| MAD        | Series  | Rolling Mean Absolute Deviation                               |
| MAV        | Series  | Generic Moving Average                                        |
| MAX        | Series  | Rolling Maximum                                               |
| MDI        | Prices  | Minus Directional Index                                       |
| MFI        | Prices  | Money Flow Index                                              |
| MIDPRICE   | Prices  | Mid Price                                                     |
| MIN        | Series  | Rolling Minimum                                               |
| NATR       | Prices  | Normalized Average True Range                                 |
| PDI        | Prices  | Plus Directional Index                                        |
| PPO        | Series  | Price Percentage Oscillator                                   |
| PRICE      | Prices  | Generic Price                                                 |
| QSF        | Series  | Quadratic Series Forecast (quadratic regression)              |
| RMA        | Series  | Rolling Moving Average (RSI style)                            |
| ROC        | Series  | Rate of Change                                                |
| RSI        | Series  | Relative Strength Index                                       |
| RVALUE     | Series  | R-Value (linear regression)                                   |
| SAR        | Prices  | Parabolic Stop and Reverse                                    |
| SIGN       | Series  | Sign                                                          |
| SLOPE      | Series  | Slope (linear regression)                                     |
| SMA        | Series  | Simple Moving Average                                         |
| STDEV      | Series  | Standard Deviation                                            |
| STEP       | Series  | Step Function                                                 |
| STOCH      | Prices  | Stochastic Oscillator                                         |
| STREAK     | Series  | Consecutive streak of values above zero                       |
| SUM        | Series  | Rolling sum                                                   |
| TEMA       | Series  | Triple Exponential Moving Average                             |
| TRANGE     | Prices  | True Range                                                    |
| TSF        | Series  | Time Series Forecast (linear regression)                      |
| TYPPRICE   | Prices  | Typical Price                                                 |
| UPDOWN     | Series  | Flag for value crossing up & down levels                      |
| WCLPRICE   | Prices  | Weighted Close Price                                          |
| WMA        | Series  | Weighted Moving Average                                       |


## Example Notebooks

Example notebooks are available in the `examples` folder.


## Related Projects

- [ta-lib](https://github.com/mrjbq7/ta-lib) Python wrapper for TA-Lib
- [pandas-ta](https://github.com/twopirllc/pandas-ta) Technical Analysis Indicators for pandas
- [ta](https://github.com/bukosabino/ta) Technical Analysis Library for pandas
- [finta](https://github.com/peerchemist/finta) Financial Technical Analysis for pandas
- [qtalib](https://github.com/josephchenhk/qtalib) Quantitative Technical Analysis Library
- [polars-ta](https://github.com/wukan1986/polars_ta) Technical Analysis Indicators for polars
- [polars-talib](https://github.com/Yvictor/polars_ta_extension) Polars extension for Ta-Lib: Support Ta-Lib functions in Polars expressions


