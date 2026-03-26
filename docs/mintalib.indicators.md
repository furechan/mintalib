# mintalib.indicators

Indicators offer a composable interface where a calculation routine is bound with its parameters.

An indicator instance is a callable and can be applied to prices or series data as if it were a function e.g. `SMA(50)(prices)`.

Indicators also support the `@` operator to apply them to their input data e.g. `SMA(50) @ prices` or to chain them together e.g. `ROC(1) @ EMA(20)`.

---

### `ABS(*, item: str = None)`

Absolute Value

### `ADX(period: int = 14)`

Average Directional Index

Args:
    period (int) : time period, default 14

### `ALMA(period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, item: str = None)`

Arnaud Legoux Moving Average

### `ATR(period: int = 14)`

Average True Range

Args:
    period (int) : time period, default 14

### `AVGPRICE()`

Average Price

Value of (open + high + low + close) / 4

### `BBANDS(period: int = 20, nbdev: float = 2.0)`

Bollinger Bands

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### `BBP(period: int = 20, nbdev: float = 2.0)`

Bollinger Bands Percent (%B)

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### `BBW(period: int = 20, nbdev: float = 2.0)`

Bollinger Bands Width

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### `BOP(period: int = 20)`

Balance of Power

Args:
    period (int) : time period, default 20

### `CCI(period: int = 20)`

Commodity Channel Index

Args:
    period (int) : time period, default 20

### `CLAG(period: int = 1, *, item: str = None)`

Confirmation Lag

Changes value only after a confirmation period 

Args:
    period (int) : time period, default 1

### `CMF(period: int = 20)`

Chaikin Money Flow

Args:
    period (int) : time period, default 20

### `CROSSOVER(level: float = 0.0, *, item: str = None)`

Cross Over

Yields a value of 1 at the point where series crosses over level

Args:
    level (float) : level to cross, default 0.0

### `CROSSUNDER(level: float = 0.0, *, item: str = None)`

Cross Under

Yields a value of 1 at the point where series crosses under level

Args:
    level (float) : level to cross, default 0.0

### `CURVE(period: int = 20, *, item: str = None)`

Curve (quadratic regression)

### `DEMA(period: int, *, item: str = None)`

Double Exponential Moving Average

Args:
    period (int) : time period, required

### `DIFF(period: int = 1, *, item: str = None)`

Difference

Difference between current value and the one offset by period

Args:
    period (int) : time period, default 1

### `DMI(period: int = 14)`

Directional Movement Indicator

Args:
    period (int) : time period, default 14

### `EMA(period: int, *, adjust: bool = False, item: str = None)`

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

Expression Eval (pandas only)

Args:
    expr (str) : expression to eval

### `EXP(*, item: str = None)`

Exponential

### `FLAG(*, item: str = None)`

Flag Value

Flag value of 1 for positive, 0 for zero or negative, and NaN otherwize

### `HMA(period: int, *, item: str = None)`

Hull Moving Average

Args:
    period (int) : time period, required

### `KAMA(period: int = 10, fastn: int = 2, slown: int = 30, *, item: str = None)`

Kaufman Adaptive Moving Average

Args:
    period (int) : time period for efficiency ratio, default 10
    fastn (int) : time period for fast moving average, default, 2
    slown (int) : time period for slow moving average, default 30

### `KELTNER(period: int = 20, nbatr: float = 2.0)`

Keltner Channel

Args:
    period (int) : time period, default 20
    nbatr (float) : channel width in number of atrs, default 2.0

### `KER(period: int = 10, *, item: str = None)`

Kaufman Efficiency Ratio

Args:
    period (int) : time period, default 10

### `LAG(period: int, *, item: str = None)`

Lag Function

Args:
    period (int) : time period, required

### `LOG(*, item: str = None)`

Logarithm

### `LROC(period: int = 1, *, item: str = None)`

Logarithmic Rate of Change

Equivalent to the difference of log values

Args:
    period (int) : time period, default 1
    when negative the calculation is shifted back

### `MACD(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None)`

Moving Average Convergence Divergence

Args:
    n1 (int) : show time period, default 12
    n2 (int) : long time periodm, default 26
    n3 (int) : signal time period, default 9  

Outputs:
    macd, macdsignal, macdhist

### `MACDV(n1: int = 12, n2: int = 26, n3: int = 9)`

Moving Average Convergence Divergence - Volatility Normalized

Args:
    n1 (int) : show time period, default 12
    n2 (int) : long time periodm, default 26
    n3 (int) : signal time period, default 9  

Outputs:
    macdv, macdvsignal, macdvhist

### `MAD(period: int = 14, *, item: str = None)`

Rolling Mean Absolute Deviation

### `MAV(period: int = 20, *, ma_type: str = 'SMA', item: str = None)`

Generic Moving Average

Moving average computed according to ma_type

Args:
    ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
            defaults to 'SMA'

### `MAX(period: int, *, item: str = None)`

Rolling Maximum

### `MDI(period: int = 14)`

Minus Directional Index

Args:
    period (int) : time period, default 14

### `MFI(period: int = 14)`

Money Flow Index 

Args:
    period (int) : time period, default 14

### `MIDPRICE()`

Mid Price

Value of (high + low) / 2

### `MIN(period: int, *, item: str = None)`

Rolling Minimum

Args:
    period (int) : time period, required

### `NATR(period: int = 14)`

Average True Range (normalized)

Args:
    period (int) : time period, default 14

### `PDI(period: int = 14)`

Plus Directional Index

Args:
    period (int) : time period, default 14

### `PPO(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None)`

Price Percentage Oscillator

Args:
    n1 (int) : short time period, default 12
    n2 (int) : long time period, default 26
    n3 (int) : signal time period, default 9

Outputs:
    ppo, pposignal, ppohist

### `PRICE(item: str = None)`

Generic Price 

Args:
    item (str) : one of 'open', 'high', 'low', 'close',
        'avg', 'mid', 'typ', 'wcl' defaults to 'close'

### `QSF(period: int = 20, offset: int = 0, *, item: str = None)`

Quadratic Series Forecast (quadratic regression)

Args:
    period (int) : time period, default 20

### `RMA(period: int, *, item: str = None)`

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

### `ROC(period: int = 1, *, item: str = None)`

Rate of Change

Args:
    period (int) : time period, default 1
    when negative the calculation is shifted back

### `RSI(period: int = 14, *, item: str = None)`

Relative Strength Index

Args:
    period (int) : time period, default 14

### `RVALUE(period: int = 20, *, item: str = None)`

R-Value (linear regression)

Args:
    period (int) : time period, default 20

### `SAR(afs: float = 0.02, maxaf: float = 0.2)`

Parabolic Stop and Reverse

Args:
    afs (float) : starting acceleration factor, default 0.02
    maxaf (float) : maximum acceleration factor, default 0.2

### `SHIFT(period: int, *, item: str = None)`

Shift Function

Args:
    period (int) : time period, required

### `SIGN(*, item: str = None)`

Sign

### `SLOPE(period: int = 20, *, item: str = None)`

Slope (linear regression)

Args:
    period (int) : time period, default 20

### `SMA(period: int, *, item: str = None)`

Simple Moving Average

Args:
    period (int) : time period, required

### `STDEV(period: int = 20, *, item: str = None)`

Standard Deviation

Args:
    period (int) : time period, default 20

### `STEP(threshold: float = 1.0, *, item: str = None)`

Step Function

Limit value changes to threshold (in absolute value)

Args:
    threshold (float) : threshold value, default 1.0

### `STOCH(period: int = 14, fastn: int = 3, slown: int = 3)`

Stochastic Oscillator

Args:
    period (int) :  time period of window, default, 14
    fastn (int) : time period of fast average, default 3
    slown (int) : time period of slow average, default 3

### `STREAK(*, item: str = None)`

Consecutive streak of values above zero

### `SUM(period: int, *, item: str = None)`

Rolling sum

Args:
    period (int) : time period, required

### `TEMA(period: int = 20, *, item: str = None)`

Triple Exponential Moving Average

Args:
    period (int) : time period, default 20

### `TRANGE(*, log_prices: bool = False, percent: bool = False)`

True Range

Args:
    log_prices (bool) : whether to apply log to prices before calculation
    percent (bool) : result as percentage of price

### `TSF(period: int = 20, offset: int = 0, *, item: str = None)`

Time Series Forecast (linear regression)

Args:
    period (int) : time period, default 20

### `TYPPRICE()`

Typical Price

Value of (high + low + close ) / 3

### `UPDOWN(up_level: float = 0.0, down_level: float = 0.0, *, item: str = None)`

Flag for value crossing up & down levels

Args:
    up_level (float) : flag set at 1 above that level
    down_level (float) : flag set at 0 below that level

### `WCLPRICE()`

Weighted Close Price

Value of (high + low + 2 * close) / 4

### `WMA(period: int, *, item: str = None)`

Weighted Moving Average
    
Args:
    period (int) : time period, required
