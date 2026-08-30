# Minimal Technical Analysis Library for Python

This package offers a curated list of technical analysis indicators implemented in `Cython` for optimal performance. The library is built around `numpy` arrays and provides interfaces for eager NumPy/pandas/polars calculations, composable pandas indicators, and native polars expressions.

> [!NOTE]
> This project is experimental and the interface can change.


## Interfaces

Mintalib offers three equivalent calculation interfaces for different workflows:

- **Functions** (`mintalib.functions`) — eager functions for NumPy arrays and pandas or polars objects.
- **Indicators** (`mintalib.indicators`) — composable pandas indicators that bind a calculation with its parameters.
- **Expressions** (`mintalib.expressions`) — composable expression factories for polars-native workflows.


## Conventions

Prices DataFrames are expected to have lower case column names `open`, `high`, `low`, `close`, `volume`. If your DataFrame has different column name capitalization you can use the `normalize_prices` utility function to normalize the column names.

```python
from mintalib.utils import normalize_prices

prices = normalize_prices(rawprices)
```


## Functions

Concrete functions are available from the `mintalib.functions` module with names in lower case like `sma`, `atr`, `macd`, etc.

Functions accept NumPy arrays, pandas objects, or polars objects as appropriate and return the same eager container type when possible. Functions that use multiple price columns take them as separate arguments in conventional OHLCV order.


```python
import mintalib.functions as ta

prices = ... # pandas or polars DataFrame

sma = ta.sma(prices['close'], 50)
atr = ta.atr(prices['high'], prices['low'], prices['close'], period=14)
```


## Composable Indicators

For workflows that benefit from reusable or chained calculations, `mintalib.indicators` binds a function and its parameters into a callable object.

Indicators work with pandas DataFrames and Series. They are callable, and series-output indicators chain with `|`.

```python
from mintalib.indicators import SMA, EMA, ROC, RSI, MACD

prices = ... # pandas DataFrame

result = prices.assign(
    ema20 = EMA(20),
    rsi = RSI(14),
    trend = EMA(20) | ROC(1)
)
```

## Expressions

Polars expression factories are available from `mintalib.expressions` with upper-case names such as `SMA`, `EMA`, `ATR`, and `MACD`.

Series calculations default to the `close` column and prices calculations read the full DataFrame when `src` is omitted. A column name or polars expression can be supplied through `src`, and a leading expression is accepted for composition with `Expr.pipe`. Multi-output calculations such as `MACD` return a polars struct expression.

```python
from mintalib.expressions import EMA, ATR, ROC, MACD

prices = ... # polars DataFrame

result = prices.with_columns(
    ema20 = EMA(20),
    atr = ATR(14),
    trend = EMA(20).pipe(ROC, 1),
    macd = MACD()
)
```

## List of Indicators

<!-- indicators:start -->
| Name           | Input   | Description                                                   |
|:---------------|:--------|:--------------------------------------------------------------|
| ABS            | Series  | Absolute Value                                                |
| ADX            | High    | Average Directional Index                                     |
| ALMA           | Series  | Arnaud Legoux Moving Average                                  |
| ATR            | High    | Average True Range                                            |
| AVGPRICE       | Open    | Average Price                                                 |
| BBANDS         | Series  | Bollinger Bands                                               |
| BBP            | Series  | Bollinger Bands Percent (%B)                                  |
| BBW            | Series  | Bollinger Bands Width                                         |
| BOP            | Open    | Balance of Power                                              |
| CCI            | High    | Commodity Channel Index                                       |
| CLAG           | Series  | Confirmation Lag                                              |
| CMF            | High    | Chaikin Money Flow                                            |
| CROSSOVER      | Series  | Cross Over                                                    |
| CROSSUNDER     | Series  | Cross Under                                                   |
| DEMA           | Series  | Double Exponential Moving Average                             |
| DIFF           | Series  | Difference                                                    |
| DMI            | High    | Directional Movement Indicator                                |
| DONCHIAN       | High    | Donchian Channel                                              |
| EMA            | Series  | Exponential Moving Average                                    |
| EXP            | Series  | Exponential                                                   |
| FLAG           | Series  | Flag Value                                                    |
| HMA            | Series  | Hull Moving Average                                           |
| KAMA           | Series  | Kaufman Adaptive Moving Average                               |
| KELTNER        | High    | Keltner Channel                                               |
| KER            | Series  | Kaufman Efficiency Ratio                                      |
| LAG            | Series  | Lag Function                                                  |
| LINREG         | Series  | Linear Regression (least squares moving average)              |
| LINREG_RMSE    | Series  | Linear Regression Root Mean Square Error                      |
| LINREG_RVALUE  | Series  | Linear Regression R-Value                                     |
| LINREG_SLOPE   | Series  | Linear Regression Slope                                       |
| LOG            | Series  | Logarithm                                                     |
| LROC           | Series  | Logarithmic Rate of Change                                    |
| MACD           | Series  | Moving Average Convergence Divergence                         |
| MACDV          | High    | Moving Average Convergence Divergence - Volatility Normalized |
| MAD            | Series  | Rolling Mean Absolute Deviation                               |
| MAV            | Series  | Generic Moving Average                                        |
| MAX            | Series  | Rolling Maximum                                               |
| MDI            | High    | Minus Directional Index                                       |
| MEDPRICE       | High    | Median Price                                                  |
| MFI            | High    | Money Flow Index                                              |
| MIN            | Series  | Rolling Minimum                                               |
| NATR           | High    | Normalized Average True Range                                 |
| OBV            | Close   | On-Balance Volume                                             |
| PDI            | High    | Plus Directional Index                                        |
| PPO            | Series  | Price Percentage Oscillator                                   |
| QUADREG        | Series  | Quadratic Regression (parabolic moving average)               |
| QUADREG_CURVE  | Series  | Quadratic Regression Curve                                    |
| QUADREG_RMSE   | Series  | Quadratic Regression Root Mean Square Error                   |
| QUADREG_RVALUE | Series  | Quadratic Regression R-Value                                  |
| QUADREG_SLOPE  | Series  | Quadratic Regression Slope                                    |
| RMA            | Series  | Rolling Moving Average (RSI style)                            |
| ROC            | Series  | Rate of Change                                                |
| ROCP           | Series  | Rate of Change Percentage                                     |
| RSI            | Series  | Relative Strength Index                                       |
| SAR            | High    | Parabolic Stop and Reverse                                    |
| SIGN           | Series  | Sign                                                          |
| SMA            | Series  | Simple Moving Average                                         |
| STDEV          | Series  | Standard Deviation                                            |
| STEP           | Series  | Step Function                                                 |
| STOCH          | High    | Stochastic Oscillator                                         |
| STREAK         | Series  | Consecutive streak of values above zero                       |
| SUM            | Series  | Rolling sum                                                   |
| TEMA           | Series  | Triple Exponential Moving Average                             |
| TRANGE         | High    | True Range                                                    |
| TYPPRICE       | High    | Typical Price                                                 |
| UPDOWN         | Series  | Flag for value crossing up & down levels                      |
| WCLPRICE       | High    | Weighted Close Price                                          |
| WMA            | Series  | Weighted Moving Average                                       |
| ZLEMA          | Series  | Zero-Lag Exponential Moving Average                           |
<!-- indicators:end -->


## Example Notebooks

Example notebooks are available in the `examples` folder.




## Installation

```console
pip install mintalib
```

Mintalib requires Python 3.11 or newer. The base install includes only NumPy; add `pandas` and/or `polars` for their corresponding objects and interfaces.

Prebuilt `cp311-abi3` wheels are available for regular CPython 3.11 and newer on Linux (x86_64 and ARM64), macOS (Intel and Apple silicon), and Windows (x64). Supported installations therefore do not need a local C compiler.


## Dependencies

- python >= 3.11
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
- [polars-talib](https://github.com/Yvictor/polars_ta_extension) Polars extension for TA-Lib
