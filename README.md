# Minimal Technical Analysis Library for Python

This package offers a curated list of technical analysis indicators implemented in `Cython` for optimal performance. The library is built around `numpy` arrays and offers a variety of interfaces for `pandas` and `polars` dataframes and series.

> [!WARNING]
> This project is experimental and the interface is likely to change.


## Interfaces

Mintalib offers three interfaces for different workflows:

- **Functions** (`mintalib.functions`) — concrete functions compatible with both polars and pandas.
- **Polars Expressions** (`mintalib.expressions`) — Composable polars expression factory methods, best for polars-native workflows
- **Pandas Indicators** (`mintalib.indicators`) — Pandas only composable indicatos that bind an indicators with their calculation parameters.


## Conventions

Prices data frames (either pandas or polars) are expeted to have lower case columns names `open`, `high`, `low`, `close`, `volume`. If your dataframe has different column name capitalization you can use the `normalize_prices` utility method to normalize the columns names.

```python
from mintalib.utils import normalize_prices

prices = normalize_prices(rawprices)
```


## Functions

Concrete functions are available from the `mintalib.functions` module with names in lower case like `sma`, `atr`, `macd`, etc.

Functions are polyvalent, they can be applied equaly to pandas or polars data interchangeably.

The first parameter of a function is either `prices` or `series` depending on whether
the function expects a dataframe of prices or a single series.


```python
import mintalib.functions as ta

prices = ... # pandas/polars DataFrame

sma = ta.sma(prices['close'], 50)
atr = ta.atr(prices, 14)
```


## Expressions

Mintalib offers expression factory methods via the `mintalib.expressions` module with names in upper case like `EMA`, `SMA`, `ATR`, `MACD`, ...

The methods accept a source expression as an optional keyword-only `src` parameter.

When no source is given, series-based expressions (e.g. `EMA`, `SMA`) default to the `close` column, while prices-based ones (e.g. `ATR`, `MACD`) read the full DataFrame.

Multi-output calculations like `MACD` return a polars struct expression.

```python
from mintalib.expressions import EMA, SMA, ATR, ROC, MACD

prices = ... # polars DataFrame

prices.with_columns(
    ema=EMA(20),
    atr=ATR(14),
    trend=EMA(20).pipe(ROC, 1)   # ROC(1) applied to EMA(20)
)
```

The source expression can also be passed as the first parameter to facilitate pipelining with the polars `pipe` method., e.g. `EMA(20).pipe(ROC, 1)` applies `ROC(1)` on top of `EMA(20)`. 



## Indicators

Indicators offer a composable interface where a computation method is bound with its parameters into a callable object. Indicators are accessible from the `mintalib.indicators` module with names in upper case like `EMA`, `SMA`, `ATR`, `MACD`, etc ...

Indicators work only on pandas DataFrames and Series.

An indicator instance is callable, ss you can use it as a function: `SMA(50)(prices)`. 

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



## Related Projects

- [ta-lib](https://github.com/mrjbq7/ta-lib) Python wrapper for TA-Lib
- [pandas-ta](https://github.com/twopirllc/pandas-ta) Technical Analysis Indicators for pandas
- [ta](https://github.com/bukosabino/ta) Technical Analysis Library for pandas
- [finta](https://github.com/peerchemist/finta) Financial Technical Analysis for pandas
- [qtalib](https://github.com/josephchenhk/qtalib) Quantitative Technical Analysis Library
- [polars-ta](https://github.com/wukan1986/polars_ta) Technical Analysis Indicators for polars
- [polars-talib](https://github.com/Yvictor/polars_ta_extension) Polars extension for Ta-Lib: Support Ta-Lib functions in Polars expressions


