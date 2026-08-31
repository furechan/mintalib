# Minimal Technical Analysis Library for Python

This package offers a curated list of technical analysis indicators implemented in `Cython` for optimal performance. The library is built around `numpy` arrays and provides interfaces for `numpy`, `pandas` and `polars`.

> [!NOTE]
> This project is experimental and the interface can change.

> [!IMPORTANT]
> Function signatures have changed: multi-input functions no longer accept a `prices` DataFrame. Pass the required columns as separate arguments instead. For example, use `atr(prices["high"], prices["low"], prices["close"])`. See the indicator table below for the data inputs required by each function.


## Interfaces

Mintalib offers three dedicated interfaces for different workflows:

- **Functions** (`mintalib.functions`) — eager functions for NumPy arrays and pandas or polars series.
- **Indicators** (`mintalib.indicators`) — composable indicators for pandas-based workflows.
- **Expressions** (`mintalib.expressions`) — composable expression factories for polars-native workflows.


## Conventions

Indicators and Expressions expect prices DataFrames to have lowercase column names such as `open`, `high`, `low`, `close`, and `volume`. If your data uses different capitalization, use the `normalize_prices` utility function to normalize its column names.

```python
from mintalib.utils import normalize_prices

prices = normalize_prices(rawprices)
```


## Functions

Concrete functions are available from the `mintalib.functions` module with names in lower case like `sma`, `atr`, `macd`, etc.

Functions accept NumPy arrays, pandas Series, or polars Series as inputs. Single-output functions preserve the input container type when possible; multi-output functions return an appropriate tabular or named result. Function signatures place data inputs first—for example, `series` or `high`, `low`, `close`—followed by parameters such as `period`.


```python
import mintalib.functions as ta

prices = ... # pandas or polars DataFrame

sma = ta.sma(prices['close'], period=50)
atr = ta.atr(prices['high'], prices['low'], prices['close'], period=14)
macd = ta.macd(prices['close'])  # macd, macdsignal, macdhist result
```


## Indicators (pandas only)

Indicators are available from `mintalib.indicators` with upper-case names such as `SMA`, `EMA`, `ATR`, and `MACD`.

Indicators bind calculation functions and their parameters together into callable objects. They are particularly useful with pandas `DataFrame.assign`.

```python
from mintalib.indicators import SMA, EMA, ROC, RSI, MACD

prices = ... # pandas DataFrame

result = prices.assign(
    ema20 = EMA(20),
    rsi = RSI(14),
    trend = EMA(20) | ROC(1)
)
```

## Expressions (polars only)

Polars expression factories are available from `mintalib.expressions` with upper-case names such as `SMA`, `EMA`, `ATR`, and `MACD`.

Their signature is parameters first like `period` followed by optional expression inputs like `src` for single series indicators, or `open`, `high`, `low`, `close`, `volume` for multi-input expressions.

Series expressions can be composed with the `.pipe` method, as in `pl.col("close").pipe(EMA, 20)`. Multi-output calculations such as `MACD` return a polars struct expression that you can unpack with `.struct.unnest()`.

```python
from mintalib.expressions import EMA, ATR, ROC, MACD

prices = ... # polars DataFrame

result = prices.with_columns(
    EMA(20).alias("ema"),
    ATR(14).alias("atr"),
    EMA(20).pipe(ROC, 1).alias("trend"),
    MACD().struct.unnest()
)
```

## List of Indicators

<!-- indicators:start -->
| Name           | Data inputs              | Description                                                   |
|:---------------|:-------------------------|:--------------------------------------------------------------|
| ABS            | series                   | Absolute Value                                                |
| ADX            | high, low, close         | Average Directional Index                                     |
| ALMA           | series                   | Arnaud Legoux Moving Average                                  |
| ATR            | high, low, close         | Average True Range                                            |
| AVGPRICE       | open, high, low, close   | Average Price                                                 |
| BBANDS         | series                   | Bollinger Bands                                               |
| BBP            | series                   | Bollinger Bands Percent (%B)                                  |
| BBW            | series                   | Bollinger Bands Width                                         |
| BOP            | open, high, low, close   | Balance of Power                                              |
| CCI            | high, low, close         | Commodity Channel Index                                       |
| CLAG           | series                   | Confirmation Lag                                              |
| CMF            | high, low, close, volume | Chaikin Money Flow                                            |
| CROSSOVER      | series                   | Cross Over                                                    |
| CROSSUNDER     | series                   | Cross Under                                                   |
| DEMA           | series                   | Double Exponential Moving Average                             |
| DIFF           | series                   | Difference                                                    |
| DMI            | high, low, close         | Directional Movement Indicator                                |
| DONCHIAN       | high, low                | Donchian Channel                                              |
| EMA            | series                   | Exponential Moving Average                                    |
| EXP            | series                   | Exponential                                                   |
| FLAG           | series                   | Flag Value                                                    |
| HMA            | series                   | Hull Moving Average                                           |
| KAMA           | series                   | Kaufman Adaptive Moving Average                               |
| KELTNER        | high, low, close         | Keltner Channel                                               |
| KER            | series                   | Kaufman Efficiency Ratio                                      |
| LAG            | series                   | Lag Function                                                  |
| LINREG         | series                   | Linear Regression (least squares moving average)              |
| LINREG_RMSE    | series                   | Linear Regression Root Mean Square Error                      |
| LINREG_RVALUE  | series                   | Linear Regression R-Value                                     |
| LINREG_SLOPE   | series                   | Linear Regression Slope                                       |
| LOG            | series                   | Logarithm                                                     |
| LROC           | series                   | Logarithmic Rate of Change                                    |
| MACD           | series                   | Moving Average Convergence Divergence                         |
| MACDV          | high, low, close         | Moving Average Convergence Divergence - Volatility Normalized |
| MAD            | series                   | Rolling Mean Absolute Deviation                               |
| MAV            | series                   | Generic Moving Average                                        |
| MAX            | series                   | Rolling Maximum                                               |
| MDI            | high, low, close         | Minus Directional Index                                       |
| MEDPRICE       | high, low                | Median Price                                                  |
| MFI            | high, low, close, volume | Money Flow Index                                              |
| MIN            | series                   | Rolling Minimum                                               |
| NATR           | high, low, close         | Normalized Average True Range                                 |
| OBV            | close, volume            | On-Balance Volume                                             |
| PDI            | high, low, close         | Plus Directional Index                                        |
| PPO            | series                   | Price Percentage Oscillator                                   |
| QUADREG        | series                   | Quadratic Regression (parabolic moving average)               |
| QUADREG_CURVE  | series                   | Quadratic Regression Curve                                    |
| QUADREG_RMSE   | series                   | Quadratic Regression Root Mean Square Error                   |
| QUADREG_RVALUE | series                   | Quadratic Regression R-Value                                  |
| QUADREG_SLOPE  | series                   | Quadratic Regression Slope                                    |
| RMA            | series                   | Rolling Moving Average (RSI style)                            |
| ROC            | series                   | Rate of Change                                                |
| ROCP           | series                   | Rate of Change Percentage                                     |
| RSI            | series                   | Relative Strength Index                                       |
| SAR            | high, low                | Parabolic Stop and Reverse                                    |
| SIGN           | series                   | Sign                                                          |
| SMA            | series                   | Simple Moving Average                                         |
| STDEV          | series                   | Standard Deviation                                            |
| STEP           | series                   | Step Function                                                 |
| STOCH          | high, low, close         | Stochastic Oscillator                                         |
| STREAK         | series                   | Consecutive streak of values above zero                       |
| SUM            | series                   | Rolling sum                                                   |
| TEMA           | series                   | Triple Exponential Moving Average                             |
| TRANGE         | high, low, close         | True Range                                                    |
| TYPPRICE       | high, low, close         | Typical Price                                                 |
| UPDOWN         | series                   | Flag for value crossing up & down levels                      |
| WCLPRICE       | high, low, close         | Weighted Close Price                                          |
| WMA            | series                   | Weighted Moving Average                                       |
| ZLEMA          | series                   | Zero-Lag Exponential Moving Average                           |
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
