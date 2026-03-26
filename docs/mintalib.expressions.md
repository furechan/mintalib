# mintalib.expressions

Polars Expression Factory Methods

---

### `IntoExpr: TypeAlias`

Type alias for polars expressions accepted as inputs (pl.Expr, column name, or None).

### `CLOSE`

Expression for the close price column.

### `OHLC`

Expression for open, high, low, close columns as a struct.

### `ABS(*, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Absolute Value

### `ADX(period: int = 14, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Average Directional Index

Args:
    period (int) : time period, default 14

### `ALMA(period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Arnaud Legoux Moving Average

### `ATR(period: int = 14, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Average True Range

Args:
    period (int) : time period, default 14

### `AVGPRICE(*, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Average Price

Value of (open + high + low + close) / 4

### `BBANDS(period: int = 20, nbdev: float = 2.0, *, src: polars.expr.expr.Expr | str | None = None) -> tuple`

Bollinger Bands

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### `BBP(period: int = 20, nbdev: float = 2.0, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Bollinger Bands Percent (%B)

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### `BBW(period: int = 20, nbdev: float = 2.0, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Bollinger Bands Width

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### `BOP(period: int = 20, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Balance of Power

Args:
    period (int) : time period, default 20

### `CCI(period: int = 20, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Commodity Channel Index

Args:
    period (int) : time period, default 20

### `CLAG(period: int = 1, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Confirmation Lag

Changes value only after a confirmation period 

Args:
    period (int) : time period, default 1

### `CMF(period: int = 20, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Chaikin Money Flow

Args:
    period (int) : time period, default 20

### `CROSSOVER(level: float = 0.0, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Cross Over

Yields a value of 1 at the point where series crosses over level

Args:
    level (float) : level to cross, default 0.0

### `CROSSUNDER(level: float = 0.0, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Cross Under

Yields a value of 1 at the point where series crosses under level

Args:
    level (float) : level to cross, default 0.0

### `CURVE(period: int = 20, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Curve (quadratic regression)

### `DEMA(period: int, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Double Exponential Moving Average

Args:
    period (int) : time period, required

### `DIFF(period: int = 1, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Difference

Difference between current value and the one offset by period

Args:
    period (int) : time period, default 1

### `DMI(period: int = 14, *, src: polars.expr.expr.Expr | str | None = None) -> tuple`

Directional Movement Indicator

Args:
    period (int) : time period, default 14

### `EMA(period: int, *, adjust: bool = False, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

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

### `EXP(*, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Exponential

### `FLAG(*, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Flag Value

Flag value of 1 for positive, 0 for zero or negative, and NaN otherwize

### `HMA(period: int, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Hull Moving Average

Args:
    period (int) : time period, required

### `KAMA(period: int = 10, fastn: int = 2, slown: int = 30, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Kaufman Adaptive Moving Average

Args:
    period (int) : time period for efficiency ratio, default 10
    fastn (int) : time period for fast moving average, default, 2
    slown (int) : time period for slow moving average, default 30

### `KELTNER(period: int = 20, nbatr: float = 2.0, *, src: polars.expr.expr.Expr | str | None = None) -> tuple`

Keltner Channel

Args:
    period (int) : time period, default 20
    nbatr (float) : channel width in number of atrs, default 2.0

### `KER(period: int = 10, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Kaufman Efficiency Ratio

Args:
    period (int) : time period, default 10

### `LAG(period: int, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Lag Function

Args:
    period (int) : time period, required

### `LOG(*, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Logarithm

### `LROC(period: int = 1, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Logarithmic Rate of Change

Equivalent to the difference of log values

Args:
    period (int) : time period, default 1
    when negative the calculation is shifted back

### `MACD(n1: int = 12, n2: int = 26, n3: int = 9, *, src: polars.expr.expr.Expr | str | None = None) -> tuple`

Moving Average Convergence Divergence

Args:
    n1 (int) : show time period, default 12
    n2 (int) : long time periodm, default 26
    n3 (int) : signal time period, default 9  

Outputs:
    macd, macdsignal, macdhist

### `MACDV(n1: int = 12, n2: int = 26, n3: int = 9, *, src: polars.expr.expr.Expr | str | None = None) -> tuple`

Moving Average Convergence Divergence - Volatility Normalized

Args:
    n1 (int) : show time period, default 12
    n2 (int) : long time periodm, default 26
    n3 (int) : signal time period, default 9  

Outputs:
    macdv, macdvsignal, macdvhist

### `MAD(period: int = 14, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Rolling Mean Absolute Deviation

### `MAV(period: int = 20, *, ma_type: str = 'SMA', src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Generic Moving Average

Moving average computed according to ma_type

Args:
    ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
            defaults to 'SMA'

### `MAX(period: int, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Rolling Maximum

### `MDI(period: int = 14, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Minus Directional Index

Args:
    period (int) : time period, default 14

### `MFI(period: int = 14, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Money Flow Index 

Args:
    period (int) : time period, default 14

### `MIDPRICE(*, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Mid Price

Value of (high + low) / 2

### `MIN(period: int, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Rolling Minimum

Args:
    period (int) : time period, required

### `NATR(period: int = 14, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Average True Range (normalized)

Args:
    period (int) : time period, default 14

### `PDI(period: int = 14, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Plus Directional Index

Args:
    period (int) : time period, default 14

### `PPO(n1: int = 12, n2: int = 26, n3: int = 9, *, src: polars.expr.expr.Expr | str | None = None) -> tuple`

Price Percentage Oscillator

Args:
    n1 (int) : short time period, default 12
    n2 (int) : long time period, default 26
    n3 (int) : signal time period, default 9

Outputs:
    ppo, pposignal, ppohist

### `PRICE(item: str = None, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Generic Price 

Args:
    item (str) : one of 'open', 'high', 'low', 'close',
        'avg', 'mid', 'typ', 'wcl' defaults to 'close'

### `QSF(period: int = 20, offset: int = 0, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Quadratic Series Forecast (quadratic regression)

Args:
    period (int) : time period, default 20

### `RMA(period: int, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

### `ROC(period: int = 1, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Rate of Change

Args:
    period (int) : time period, default 1
    when negative the calculation is shifted back

### `RSI(period: int = 14, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Relative Strength Index

Args:
    period (int) : time period, default 14

### `RVALUE(period: int = 20, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

R-Value (linear regression)

Args:
    period (int) : time period, default 20

### `SAR(afs: float = 0.02, maxaf: float = 0.2, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Parabolic Stop and Reverse

Args:
    afs (float) : starting acceleration factor, default 0.02
    maxaf (float) : maximum acceleration factor, default 0.2

### `SHIFT(period: int, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Shift Function

Args:
    period (int) : time period, required

### `SIGN(*, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Sign

### `SLOPE(period: int = 20, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Slope (linear regression)

Args:
    period (int) : time period, default 20

### `SMA(period: int, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Simple Moving Average

Args:
    period (int) : time period, required

### `STDEV(period: int = 20, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Standard Deviation

Args:
    period (int) : time period, default 20

### `STEP(threshold: float = 1.0, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Step Function

Limit value changes to threshold (in absolute value)

Args:
    threshold (float) : threshold value, default 1.0

### `STOCH(period: int = 14, fastn: int = 3, slown: int = 3, *, src: polars.expr.expr.Expr | str | None = None) -> tuple`

Stochastic Oscillator

Args:
    period (int) :  time period of window, default, 14
    fastn (int) : time period of fast average, default 3
    slown (int) : time period of slow average, default 3

### `STREAK(*, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Consecutive streak of values above zero

### `SUM(period: int, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Rolling sum

Args:
    period (int) : time period, required

### `TEMA(period: int = 20, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Triple Exponential Moving Average

Args:
    period (int) : time period, default 20

### `TRANGE(*, log_prices: bool = False, percent: bool = False, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

True Range

Args:
    log_prices (bool) : whether to apply log to prices before calculation
    percent (bool) : result as percentage of price

### `TSF(period: int = 20, offset: int = 0, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Time Series Forecast (linear regression)

Args:
    period (int) : time period, default 20

### `TYPPRICE(*, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Typical Price

Value of (high + low + close ) / 3

### `UPDOWN(up_level: float = 0.0, down_level: float = 0.0, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Flag for value crossing up & down levels

Args:
    up_level (float) : flag set at 1 above that level
    down_level (float) : flag set at 0 below that level

### `WCLPRICE(*, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Weighted Close Price

Value of (high + low + 2 * close) / 4

### `WMA(period: int, *, src: polars.expr.expr.Expr | str | None = None) -> polars.expr.expr.Expr`

Weighted Moving Average
    
Args:
    period (int) : time period, required
