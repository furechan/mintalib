# Minimal Technical Analysis Library for Python

This package offers a curated list of technical analysis indicators implemented in `Cython` for optimal performance. The library is built around `numpy` arrays and offers a variety of interfaces for `pandas` and `polars` dataframes and series.

> [!WARNING]
> This project is experimental and the interface is likely to change.


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

An indicator instance can be invoked as a function or via the `@` operator as syntactic sugar.

So for example `SMA(50) @ prices` can be used to compute the 50 period simple moving average on `prices`, in place of `SMA(50)(prices)`.

The `@` operator can also be used to chain indicators, where for example `ROC(1) @ EMA(20)` means `ROC(1)` applied to `EMA(20)`.

```python
from mintalib.indicators import SMA, EMA, ROC, RSI, MACD

prices = ... # pandas DataFrame

result = prices.assign(
    sma50 = SMA(50),
    sma200 = SMA(200),
    rsi = RSI(14),
    trend = ROC(1) @ EMA(20)
)
```

## List of Indicators

| Name       | Description                                                            |
|:-----------|:-----------------------------------------------------------------------|
| ABS        | calc_abs(series)                                                       |
| ADX        | calc_adx(prices, long period=14)                                       |
| ALMA       | calc_alma(series, long period=9, double offset=0.85, double sigma=6.0) |
| ATR        | calc_atr(prices, long period=14)                                       |
| AVGPRICE   | calc_avgprice(prices)                                                  |
| BBANDS     | calc_bbands(prices, long period=20, double nbdev=2.0)                  |
| BBP        | calc_bbp(prices, long period=20, double nbdev=2.0)                     |
| BBW        | calc_bbw(prices, long period=20, double nbdev=2.0)                     |
| BOP        | calc_bop(prices, long period=20)                                       |
| CCI        | calc_cci(prices, long period=20)                                       |
| CLAG       | calc_clag(series, long period=1)                                       |
| CMF        | calc_cmf(prices, long period=20)                                       |
| CROSSOVER  | calc_crossover(series, double level=0.0)                               |
| CROSSUNDER | calc_crossunder(series, double level=0.0)                              |
| CURVE      | calc_curve(series, long period=20)                                     |
| DEMA       | calc_dema(series, long period)                                         |
| DIFF       | calc_diff(series, long period=1)                                       |
| DMI        | calc_dmi(prices, long period=14)                                       |
| EMA        | calc_ema(series, long period, *, bool adjust=False)                    |
| EVAL       | calc_eval(prices, str expr, *, bool as_flag=False)                     |
| EXP        | calc_exp(series)                                                       |
| FLAG       | calc_flag(series)                                                      |
| HMA        | calc_hma(series, long period)                                          |
| KAMA       | calc_kama(series, int period=10, int fastn=2, int slown=30)            |
| KELTNER    | calc_keltner(prices, long period=20, double nbatr=2.0)                 |
| KER        | calc_ker(series, int period=10)                                        |
| LAG        | calc_lag(series, long period)                                          |
| LOG        | calc_log(series)                                                       |
| LROC       | calc_lroc(series, long period=1)                                       |
| MACD       | calc_macd(series, long n1=12, long n2=26, long n3=9)                   |
| MACDV      | calc_macdv(prices, long n1=12, long n2=26, long n3=9)                  |
| MAD        | calc_mad(series, int period: int = 14)                                 |
| MAV        | calc_mav(series, long period=20, *, str ma_type='SMA')                 |
| MAX        | calc_max(series, long period)                                          |
| MDI        | calc_mdi(prices, long period=14)                                       |
| MFI        | calc_mfi(prices, long period=14)                                       |
| MIDPRICE   | calc_midprice(prices)                                                  |
| MIN        | calc_min(series, long period)                                          |
| NATR       | calc_natr(prices, long period=14)                                      |
| PDI        | calc_pdi(prices, long period=14)                                       |
| PPO        | calc_ppo(series, long n1=12, long n2=26, long n3=9)                    |
| PRICE      | calc_price(prices, str item: str = None)                               |
| QSF        | calc_qsf(series, long period=20, long offset=0)                        |
| RMA        | calc_rma(series, long period)                                          |
| ROC        | calc_roc(series, long period=1)                                        |
| RSI        | calc_rsi(series, long period=14)                                       |
| RVALUE     | calc_rvalue(series, long period=20)                                    |
| SAR        | calc_sar(prices, double afs=0.02, double maxaf=0.2)                    |
| SIGN       | calc_sign(series)                                                      |
| SLOPE      | calc_slope(series, long period=20)                                     |
| SMA        | calc_sma(series, long period)                                          |
| STDEV      | calc_stdev(series, long period=20)                                     |
| STEP       | calc_step(series, double threshold: float = 1.0)                       |
| STOCH      | calc_stoch(prices, long period=14, long fastn=3, long slown=3)         |
| STREAK     | calc_streak(series)                                                    |
| SUM        | calc_sum(series, long period)                                          |
| TEMA       | calc_tema(series, long period=20)                                      |
| TRANGE     | calc_trange(prices, *, bool log_prices=False, bool percent=False)      |
| TSF        | calc_tsf(series, long period=20, long offset=0)                        |
| TYPPRICE   | calc_typprice(prices)                                                  |
| UPDOWN     | calc_updown(series, double up_level=0.0, double down_level=0.0)        |
| WCLPRICE   | calc_wclprice(prices)                                                  |
| WMA        | calc_wma(series, long period)                                          |


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


