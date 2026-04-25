# mintalib.indicators

Indicators offer a composable interface where a calculation routine is bound with its parameters.

An indicator instance is a callable and can be applied to prices or series data as if it were a function e.g. `SMA(50)(prices)`.

Indicators support the `|` operator to apply them to data e.g. `prices | SMA(50)` or to chain them together e.g. `EMA(20) | ROC(1)`.

---

### `ABS(*, item: str | None = None)`

calc_abs(series)

Absolute Value

### `ADX(period: int = 14)`

calc_adx(prices, long period=14)

Average Directional Index

Args:
    period (int) : time period, default 14

### `ALMA(period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, item: str | None = None)`

calc_alma(series, long period=9, double offset=0.85, double sigma=6.0)

Arnaud Legoux Moving Average

### `ATR(period: int = 14)`

calc_atr(prices, long period=14)

Average True Range

Args:
    period (int) : time period, default 14

### `AVGPRICE()`

calc_avgprice(prices)

Average Price

Value of (open + high + low + close) / 4

### `BBANDS(period: int = 20, nbdev: float = 2.0)`

calc_bbands(prices, long period=20, double nbdev=2.0)

Bollinger Bands

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### `BBP(period: int = 20, nbdev: float = 2.0)`

calc_bbp(prices, long period=20, double nbdev=2.0)

Bollinger Bands Percent (%B)

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### `BBW(period: int = 20, nbdev: float = 2.0)`

calc_bbw(prices, long period=20, double nbdev=2.0)

Bollinger Bands Width

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### `BOP(period: int = 20)`

calc_bop(prices, long period=20)

Balance of Power

Args:
    period (int) : time period, default 20

### `CCI(period: int = 20)`

calc_cci(prices, long period=20)

Commodity Channel Index

Args:
    period (int) : time period, default 20

### `CLAG(period: int = 1, *, item: str | None = None)`

calc_clag(series, long period=1)

Confirmation Lag

Changes value only after a confirmation period 

Args:
    period (int) : time period, default 1

### `CMF(period: int = 20)`

calc_cmf(prices, long period=20)

Chaikin Money Flow

Args:
    period (int) : time period, default 20

### `CROSSOVER(level: float = 0.0, *, item: str | None = None)`

calc_crossover(series, double level=0.0)

Cross Over

Yields a value of 1 at the point where series crosses over level

Args:
    level (float) : level to cross, default 0.0

### `CROSSUNDER(level: float = 0.0, *, item: str | None = None)`

calc_crossunder(series, double level=0.0)

Cross Under

Yields a value of 1 at the point where series crosses under level

Args:
    level (float) : level to cross, default 0.0

### `CURVE(period: int = 20, *, item: str | None = None)`

calc_curve(series, long period=20)

Curve (quadratic regression)

### `DEMA(period: int, *, item: str | None = None)`

calc_dema(series, long period)

Double Exponential Moving Average

Args:
    period (int) : time period, required

### `DIFF(period: int = 1, *, item: str | None = None)`

calc_diff(series, long period=1)

Difference

Difference between current value and the one offset by period

Args:
    period (int) : time period, default 1

### `DMI(period: int = 14)`

calc_dmi(prices, long period=14)

Directional Movement Indicator

Args:
    period (int) : time period, default 14

### `DONCHIAN(period: int = 20)`

calc_donchian(prices, long period=20)

Donchian Channel

Args:
    period (int) : time period, default 20

### `EMA(period: int, *, adjust: bool = False, item: str | None = None)`

calc_ema(series, long period, *, bool adjust=False)

Exponential Moving Average

Args:
    period (int) : time period, required
    adjust (bool) : whether to adjust weights, default False
        when true update ratio increases gradually (see formula)

Formula:
    EMA is calculated as a recursive formula
    The standard formula is ema += alpha * (value - ema)
        with alpha = 2.0 / (period + 1.0)
    The adjusted formula is ema = num/div
        where num = value + rho * num, div = 1.0 + rho * div
        with rho = 1.0 - alpha

### `EVAL(expr: str, *, as_flag: bool = False)`

calc_eval(prices, str expr, *, bool as_flag=False)

Expression Eval

Evaluates an expression against the prices dataframe.
Uses `DataFrame.eval` for pandas and `DataFrame.sql` for polars.

Args:
    expr (str) : expression to eval
    as_flag (bool) : whether to return result as a flag value

### `EXP(*, item: str | None = None)`

calc_exp(series)

Exponential

### `FLAG(*, item: str | None = None)`

calc_flag(series)

Flag Value

Flag value of 1 for positive, 0 for zero or negative, and NaN otherwize

### `HMA(period: int, *, item: str | None = None)`

calc_hma(series, long period)

Hull Moving Average

Args:
    period (int) : time period, required

### `KAMA(period: int = 10, fastn: int = 2, slown: int = 30, *, item: str | None = None)`

calc_kama(series, int period=10, int fastn=2, int slown=30)

Kaufman Adaptive Moving Average

Args:
    period (int) : time period for efficiency ratio, default 10
    fastn (int) : time period for fast moving average, default, 2
    slown (int) : time period for slow moving average, default 30

### `KELTNER(period: int = 20, nbatr: float = 2.0)`

calc_keltner(prices, long period=20, double nbatr=2.0)

Keltner Channel

Args:
    period (int) : time period, default 20
    nbatr (float) : channel width in number of atrs, default 2.0

### `KER(period: int = 10, *, item: str | None = None)`

calc_ker(series, int period=10)

Kaufman Efficiency Ratio

Args:
    period (int) : time period, default 10

### `LAG(period: int, *, item: str | None = None)`

calc_lag(series, long period)

Lag Function

Args:
    period (int) : time period, required

### `LOG(*, item: str | None = None)`

calc_log(series)

Logarithm

### `LROC(period: int = 1, *, item: str | None = None)`

calc_lroc(series, long period=1)

Logarithmic Rate of Change

Equivalent to the difference of log values

Args:
    period (int) : time period, default 1
    when negative the calculation is shifted back

### `MACD(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str | None = None)`

calc_macd(series, long n1=12, long n2=26, long n3=9)

Moving Average Convergence Divergence

Args:
    n1 (int) : short time period, default 12
    n2 (int) : long time period, default 26
    n3 (int) : signal time period, default 9  

Outputs:
    macd, macdsignal, macdhist

### `MACDV(n1: int = 12, n2: int = 26, n3: int = 9)`

calc_macdv(prices, long n1=12, long n2=26, long n3=9)

Moving Average Convergence Divergence - Volatility Normalized

Args:
    n1 (int) : short time period, default 12
    n2 (int) : long time period, default 26
    n3 (int) : signal time period, default 9  

Outputs:
    macdv, macdvsignal, macdvhist

### `MAD(period: int = 14, *, item: str | None = None)`

calc_mad(series, long period=14)

Rolling Mean Absolute Deviation

### `MAV(period: int = 20, *, ma_type: str = 'SMA', item: str | None = None)`

calc_mav(series, long period=20, *, str ma_type='SMA')

Generic Moving Average

Moving average computed according to ma_type

Args:
    ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
            defaults to 'SMA'

### `MAX(period: int, *, item: str | None = None)`

calc_max(series, long period)

Rolling Maximum

### `MDI(period: int = 14)`

calc_mdi(prices, long period=14)

Minus Directional Index

Args:
    period (int) : time period, default 14

### `MFI(period: int = 14)`

calc_mfi(prices, long period=14)

Money Flow Index 

Args:
    period (int) : time period, default 14

### `MIDPRICE()`

calc_midprice(prices)

Mid Price

Value of (high + low) / 2

### `MIN(period: int, *, item: str | None = None)`

calc_min(series, long period)

Rolling Minimum

Args:
    period (int) : time period, required

### `NATR(period: int = 14)`

calc_natr(prices, long period=14)

Average True Range (normalized)

Args:
    period (int) : time period, default 14

### `PDI(period: int = 14)`

calc_pdi(prices, long period=14)

Plus Directional Index

Args:
    period (int) : time period, default 14

### `PPO(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str | None = None)`

calc_ppo(series, long n1=12, long n2=26, long n3=9)

Price Percentage Oscillator

Args:
    n1 (int) : short time period, default 12
    n2 (int) : long time period, default 26
    n3 (int) : signal time period, default 9

Outputs:
    ppo, pposignal, ppohist

### `PRICE(item: str | None = None)`

calc_price(prices, str item: str = None)

Generic Price

Args:
    item (str) : price type, one of:
        'open', 'high', 'low', 'close' (default),
        'avg' or 'ohlc4'  — average price (open + high + low + close) / 4,
        'mid' or 'hl2'    — mid price (high + low) / 2,
        'typ' or 'hlc3'   — typical price (high + low + close) / 3,
        'wcl' or 'hlcc4'  — weighted close (high + low + 2 * close) / 4

### `QSF(period: int = 20, offset: int = 0, *, item: str | None = None)`

calc_qsf(series, long period=20, long offset=0)

Quadratic Series Forecast (quadratic regression)

Args:
    period (int) : time period, default 20

### `RMA(period: int, *, item: str | None = None)`

calc_rma(series, long period)

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

### `ROC(period: int = 1, *, item: str | None = None)`

calc_roc(series, long period=1)

Rate of Change

Args:
    period (int) : time period, default 1
    when negative the calculation is shifted back

### `RSI(period: int = 14, *, item: str | None = None)`

calc_rsi(series, long period=14)

Relative Strength Index

Args:
    period (int) : time period, default 14

### `RVALUE(period: int = 20, *, item: str | None = None)`

calc_rvalue(series, long period=20)

R-Value (linear regression)

Args:
    period (int) : time period, default 20

### `SAR(afs: float = 0.02, maxaf: float = 0.2)`

calc_sar(prices, double afs=0.02, double maxaf=0.2)

Parabolic Stop and Reverse

Args:
    afs (float) : starting acceleration factor, default 0.02
    maxaf (float) : maximum acceleration factor, default 0.2

### `SIGN(*, item: str | None = None)`

calc_sign(series)

Sign

### `SLOPE(period: int = 20, *, item: str | None = None)`

calc_slope(series, long period=20)

Slope (linear regression)

Args:
    period (int) : time period, default 20

### `SMA(period: int, *, item: str | None = None)`

calc_sma(series, long period)

Simple Moving Average

Args:
    period (int) : time period, required

### `STDEV(period: int = 20, *, item: str | None = None)`

calc_stdev(series, long period=20)

Standard Deviation

Args:
    period (int) : time period, default 20

### `STEP(threshold: float = 1.0, *, item: str | None = None)`

calc_step(series, double threshold: float = 1.0)

Step Function

Limit value changes to threshold (in absolute value)

Args:
    threshold (float) : threshold value, default 1.0

### `STOCH(period: int = 14, fastn: int = 3, slown: int = 3)`

calc_stoch(prices, long period=14, long fastn=3, long slown=3)

Stochastic Oscillator

Args:
    period (int) :  time period of window, default, 14
    fastn (int) : time period of fast average, default 3
    slown (int) : time period of slow average, default 3

### `STREAK(*, item: str | None = None)`

calc_streak(series)

Consecutive streak of values above zero

### `SUM(period: int, *, item: str | None = None)`

calc_sum(series, long period)

Rolling sum

Args:
    period (int) : time period, required

### `TEMA(period: int = 20, *, item: str | None = None)`

calc_tema(series, long period=20)

Triple Exponential Moving Average

Args:
    period (int) : time period, default 20

### `TRANGE(*, log_prices: bool = False, percent: bool = False)`

calc_trange(prices, *, bool log_prices=False, bool percent=False)

True Range

Args:
    log_prices (bool) : whether to apply log to prices before calculation
    percent (bool) : result as percentage of price

### `TSF(period: int = 20, offset: int = 0, *, item: str | None = None)`

calc_tsf(series, long period=20, long offset=0)

Time Series Forecast (linear regression)

Args:
    period (int) : time period, default 20

### `TYPPRICE()`

calc_typprice(prices)

Typical Price

Value of (high + low + close ) / 3

### `UPDOWN(up_level: float = 0.0, down_level: float = 0.0, *, item: str | None = None)`

calc_updown(series, double up_level=0.0, double down_level=0.0)

Flag for value crossing up & down levels

Args:
    up_level (float) : flag set at 1 above that level
    down_level (float) : flag set at 0 below that level

### `WCLPRICE()`

calc_wclprice(prices)

Weighted Close Price

Value of (high + low + 2 * close) / 4

### `WMA(period: int, *, item: str | None = None)`

calc_wma(series, long period)

Weighted Moving Average
    
Args:
    period (int) : time period, required
