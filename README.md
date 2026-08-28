# Minimal Technical Analysis Library for Python

This package offers a curated list of technical analysis indicators implemented in `Cython` for optimal performance. The library is built around `numpy` arrays and integrates with `pandas` DataFrames and Series.

> [!NOTE]
> This project is experimental and the interface can change.


## Interfaces

Mintalib offers two interfaces for different workflows:

- **Functions** (`mintalib.functions`) — concrete functions for arrays and pandas objects.
- **Indicators** (`mintalib.indicators`) — pandas-only composable indicators that bind an indicator with its calculation parameters.


## Conventions

Prices DataFrames are expected to have lower case column names `open`, `high`, `low`, `close`, `volume`. If your DataFrame has different column name capitalization you can use the `normalize_prices` utility function to normalize the column names.

```python
from mintalib.utils import normalize_prices

prices = normalize_prices(rawprices)
```


## Functions

Concrete functions are available from the `mintalib.functions` module with names in lower case like `sma`, `atr`, `macd`, etc.

Functions accept NumPy arrays, pandas Series, or pandas DataFrames as appropriate.

The first parameter of a function is either `prices` or `series` depending on whether
the function expects a dataframe of prices or a single series.


```python
import mintalib.functions as ta

prices = ... # pandas DataFrame

sma = ta.sma(prices['close'], 50)
atr = ta.atr(prices, 14)
```


## Composable Indicators

For workflows that benefit from reusable or chained calculations, `mintalib.indicators` binds a function and its parameters into a callable object.

Indicators work with pandas DataFrames and Series. They are callable, and chain with `|` or the equivalent `.then()` method.

```python
from mintalib.indicators import SMA, EMA, ROC, RSI, MACD

prices = ... # pandas DataFrame

result = prices.assign(
    ema20 = EMA(20),
    rsi = RSI(14),
    trend = EMA(20) | ROC(1)
)
```

## Function Reference

<!-- functions:start -->
| | |
|---|---|
| `abs(series)` | Absolute Value |
| `adx(prices, period=14)` | Average Directional Index |
| `alma(series, period=9, offset=0.85, sigma=6.0)` | Arnaud Legoux Moving Average |
| `atr(prices, period=14)` | Average True Range |
| `avgprice(prices)` | Average Price |
| `bbands(series, period=20, nbdev=2.0)` | Bollinger Bands |
| `bbp(series, period=20, nbdev=2.0)` | Bollinger Bands Percent (%B) |
| `bbw(series, period=20, nbdev=2.0)` | Bollinger Bands Width |
| `bop(prices)` | Balance of Power |
| `cci(prices, period=20)` | Commodity Channel Index |
| `clag(series, period=1)` | Confirmation Lag |
| `cmf(prices, period=20)` | Chaikin Money Flow |
| `crossover(series, level=0.0)` | Cross Over |
| `crossunder(series, level=0.0)` | Cross Under |
| `dema(series, period)` | Double Exponential Moving Average |
| `diff(series, period=1)` | Difference |
| `dmi(prices, period=14)` | Directional Movement Indicator |
| `donchian(prices, period=20)` | Donchian Channel |
| `ema(series, period, *, adjust=False)` | Exponential Moving Average |
| `exp(series)` | Exponential |
| `flag(series)` | Flag Value |
| `hma(series, period)` | Hull Moving Average |
| `kama(series, period=10, fastn=2, slown=30)` | Kaufman Adaptive Moving Average |
| `keltner(prices, period=20, nbatr=2.0)` | Keltner Channel |
| `ker(series, period=10)` | Kaufman Efficiency Ratio |
| `lag(series, period)` | Lag Function |
| `linreg(series, period=20, offset=0)` | Linear Regression (least squares moving average) |
| `linreg_rmse(series, period=20)` | Linear Regression Root Mean Square Error |
| `linreg_rvalue(series, period=20)` | Linear Regression R-Value |
| `linreg_slope(series, period=20)` | Linear Regression Slope |
| `log(series)` | Logarithm |
| `lroc(series, period=1)` | Logarithmic Rate of Change |
| `macd(series, n1=12, n2=26, n3=9)` | Moving Average Convergence Divergence |
| `macdv(prices, n1=12, n2=26, n3=9)` | Moving Average Convergence Divergence - Volatility Normalized |
| `mad(series, period=14)` | Rolling Mean Absolute Deviation |
| `mav(series, period=20, *, matype='sma')` | Generic Moving Average |
| `max(series, period)` | Rolling Maximum |
| `mdi(prices, period=14)` | Minus Directional Index |
| `medprice(prices)` | Median Price |
| `mfi(prices, period=14)` | Money Flow Index |
| `min(series, period)` | Rolling Minimum |
| `natr(prices, period=14)` | Normalized Average True Range |
| `pdi(prices, period=14)` | Plus Directional Index |
| `ppo(series, n1=12, n2=26, n3=9)` | Price Percentage Oscillator |
| `price(prices, item=None)` | Generic Price |
| `quadreg(series, period=20, offset=0)` | Quadratic Regression (parabolic moving average) |
| `quadreg_curve(series, period=20)` | Quadratic Regression Curve |
| `quadreg_rmse(series, period=20)` | Quadratic Regression Root Mean Square Error |
| `quadreg_rvalue(series, period=20)` | Quadratic Regression R-Value |
| `quadreg_slope(series, period=20, offset=0)` | Quadratic Regression Slope |
| `rma(series, period)` | Rolling Moving Average (RSI style) |
| `roc(series, period=1)` | Rate of Change |
| `rocp(series, period=1)` | Rate of Change Percentage |
| `rsi(series, period=14)` | Relative Strength Index |
| `sar(prices, afs=0.02, maxaf=0.2)` | Parabolic Stop and Reverse |
| `sign(series)` | Sign |
| `sma(series, period)` | Simple Moving Average |
| `stdev(series, period=20)` | Standard Deviation |
| `step(series, threshold=1.0)` | Step Function |
| `stoch(prices, period=14, fastn=3, slown=3)` | Stochastic Oscillator |
| `streak(series)` | Consecutive streak of values above zero |
| `sum(series, period)` | Rolling sum |
| `tema(series, period=20)` | Triple Exponential Moving Average |
| `trange(prices, *, log_prices=False, percent=False)` | True Range |
| `typprice(prices)` | Typical Price |
| `updown(series, up_level=0.0, down_level=0.0)` | Flag for value crossing up & down levels |
| `wclprice(prices)` | Weighted Close Price |
| `wma(series, period)` | Weighted Moving Average |
| `zlema(series, period)` | Zero-Lag Exponential Moving Average |
<!-- functions:end -->


## Example Notebooks

Example notebooks are available in the `examples` folder.




## Installation

```console
pip install mintalib
```

Mintalib requires Python 3.11 or newer. The base install includes only NumPy; add `pandas` to use the indicator interface or pandas objects.


## Dependencies

- python >= 3.11
- numpy
- pandas [optional]



## Related Projects

- [ta-lib](https://github.com/mrjbq7/ta-lib) Python wrapper for TA-Lib
- [pandas-ta](https://github.com/twopirllc/pandas-ta) Technical Analysis Indicators for pandas
- [ta](https://github.com/bukosabino/ta) Technical Analysis Library for pandas
- [finta](https://github.com/peerchemist/finta) Financial Technical Analysis for pandas
- [qtalib](https://github.com/josephchenhk/qtalib) Quantitative Technical Analysis Library
