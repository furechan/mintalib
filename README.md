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

- **Functions** (`mintalib.functions`) — plain functions, useful for scripting or building custom pipelines
- **Polars Expressions** (`mintalib.expressions`) — composable polars expressions, best for polars-native workflows
- **Indicators** (`mintalib.indicators`) — callable objects that bind a calculation with its parameters, work with both pandas and polars


## Functions

Calculation functions are available from the `mintalib.functions` module with names in lower case like `sma`, `atr`, `macd`, etc.

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


## Polars Expressions

Mintalib offers expression factory methods via the `mintalib.expressions` module with names in upper case like `EMA`, `SMA`, `ATR`, `MACD`, ...
The methods accept a source expression as an optional keyword-only `src` parameter.
The source expression can also be passed as the first parameter to facilitate the use with `pipe`. Multi column output calculations like `MACD` return a tuple of expressions.

```python
from mintalib.expressions import EMA, SMA, ATR, ROC, MACD

prices = ... # polars DataFrame

prices.with_columns(
    MACD(),                      # uses 'close' by default
    sma=SMA(50),
    atr=ATR(14),
    trend=EMA(50).pipe(ROC, 1)   # ROC(1) applied to EMA(50)
)
```

## Using Indicators

Indicators offer a composable interface where a calculation function is bound with its parameters into a callable object. Indicators are accessible from the `mintalib.indicators` module with names in upper case like `EMA`, `SMA`, `ATR`, `MACD`, etc ...

An indicator instance can be invoked as a function or applied to data using the `|` operator as syntactic sugar.

Indicators can also be chained with `|`, where for example `EMA(20) | ROC(1)` means `ROC(1)` applied to `EMA(20)`.

```python
from mintalib.indicators import SMA, EMA, ROC, RSI, MACD

prices = ... # pandas DataFrame

result = prices.assign(
    sma50 = SMA(50),
    sma200 = SMA(200),
    rsi = RSI(14),
    trend = EMA(20) | ROC(1)
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
| DONCHIAN   | Donchian Channel                                              |
| EMA        | Exponential Moving Average                                    |
| EVAL       | Expression Eval                                               |
| EXP        | Exponential                                                   |
| FLAG       | Flag Value                                                    |
| HMA        | Hull Moving Average                                           |
| KAMA       | Kaufman Adaptive Moving Average                               |
| KELTNER    | Keltner Channel                                               |
| KER        | Kaufman Efficiency Ratio                                      |
| LAG        | Lag Function                                                  |
| LOG        | Logarithm                                                     |
| LROC       | Logarithmic Rate of Change                                    |
| MACD       | Moving Average Convergence Divergence                         |
| MACDV      | Moving Average Convergence Divergence - Volatility Normalized |
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

Example notebooks are available in the `examples` folder.


## Related Projects

- [ta-lib](https://github.com/mrjbq7/ta-lib) Python wrapper for TA-Lib
- [pandas-ta](https://github.com/twopirllc/pandas-ta) Technical Analysis Indicators for pandas
- [ta](https://github.com/bukosabino/ta) Technical Analysis Library for pandas
- [finta](https://github.com/peerchemist/finta) Financial Technical Analysis for pandas
- [qtalib](https://github.com/josephchenhk/qtalib) Quantitative Technical Analysis Library
- [polars-ta](https://github.com/wukan1986/polars_ta) Technical Analysis Indicators for polars
- [polars-talib](https://github.com/Yvictor/polars_ta_extension) Polars extension for Ta-Lib: Support Ta-Lib functions in Polars expressions


