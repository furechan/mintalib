# mintalib.functions

Calculation functions for technical analysis indicators.

These functions are a thin wrapper arround core calculation routine that handle input and output type conversion.

The function names are all lower case like `sma`, `ema`, etc 
To avoid name conflicts it is advised to import the module as a whole with a short alias like `ta`.

---

### abs(series)

Absolute Value

### adx(prices, period: int = 14)

Average Directional Index

Args:
    period (int) : time period, default 14

### alma(series, period: int = 9, offset: float = 0.85, sigma: float = 6.0)

Arnaud Legoux Moving Average

### atr(prices, period: int = 14)

Average True Range

Args:
    period (int) : time period, default 14

### avgprice(prices)

Average Price

Value of (open + high + low + close) / 4

### bbands(prices, period: int = 20, nbdev: float = 2.0)

Bollinger Bands

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### bbp(prices, period: int = 20, nbdev: float = 2.0)

Bollinger Bands Percent (%B)

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### bbw(prices, period: int = 20, nbdev: float = 2.0)

Bollinger Bands Width

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

### bop(prices, period: int = 20)

Balance of Power

Args:
    period (int) : time period, default 20

### cci(prices, period: int = 20)

Commodity Channel Index

Args:
    period (int) : time period, default 20

### clag(series, period: int = 1)

Confirmation Lag

Changes value only after a confirmation period 

Args:
    period (int) : time period, default 1

### cmf(prices, period: int = 20)

Chaikin Money Flow

Args:
    period (int) : time period, default 20

### crossover(series, level: float = 0.0)

Cross Over

Yields a value of 1 at the point where series crosses over level

Args:
    level (float) : level to cross, default 0.0

### crossunder(series, level: float = 0.0)

Cross Under

Yields a value of 1 at the point where series crosses under level

Args:
    level (float) : level to cross, default 0.0

### curve(series, period: int = 20)

Curve (quadratic regression)

### dema(series, period: int)

Double Exponential Moving Average

Args:
    period (int) : time period, required

### diff(series, period: int = 1)

Difference

Difference between current value and the one offset by period

Args:
    period (int) : time period, default 1

### dmi(prices, period: int = 14)

Directional Movement Indicator

Args:
    period (int) : time period, default 14

### ema(series, period: int, *, adjust: bool = False)

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

### eval(prices, expr: str, *, as_flag: bool = False)

Expression Eval (pandas only)

Args:
    expr (str) : expression to eval

### exp(series)

Exponential

### flag(series)

Flag Value

Flag value of 1 for positive, 0 for zero or negative, and NaN otherwize

### hma(series, period: int)

Hull Moving Average

Args:
    period (int) : time period, required

### kama(series, period: int = 10, fastn: int = 2, slown: int = 30)

Kaufman Adaptive Moving Average

Args:
    period (int) : time period for efficiency ratio, default 10
    fastn (int) : time period for fast moving average, default, 2
    slown (int) : time period for slow moving average, default 30

### keltner(prices, period: int = 20, nbatr: float = 2.0)

Keltner Channel

Args:
    period (int) : time period, default 20
    nbatr (float) : channel width in number of atrs, default 2.0

### ker(series, period: int = 10)

Kaufman Efficiency Ratio

Args:
    period (int) : time period, default 10

### lag(series, period: int)

Lag Function

Args:
    period (int) : time period, required

### log(series)

Logarithm

### lroc(series, period: int = 1)

Logarithmic Rate of Change

Equivalent to the difference of log values

Args:
    period (int) : time period, default 1
    when negative the calculation is shifted back

### macd(series, n1: int = 12, n2: int = 26, n3: int = 9)

Moving Average Convergence Divergence

Args:
    n1 (int) : show time period, default 12
    n2 (int) : long time periodm, default 26
    n3 (int) : signal time period, default 9  

Outputs:
    macd, macdsignal, macdhist

### macdv(prices, n1: int = 12, n2: int = 26, n3: int = 9)

Moving Average Convergence Divergence - Volatility Normalized

Args:
    n1 (int) : show time period, default 12
    n2 (int) : long time periodm, default 26
    n3 (int) : signal time period, default 9  

Outputs:
    macdv, macdvsignal, macdvhist

### mad(series, period: int = 14)

Rolling Mean Absolute Deviation

### mav(series, period: int = 20, *, ma_type: str = 'SMA')

Generic Moving Average

Moving average computed according to ma_type

Args:
    ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
            defaults to 'SMA'

### max(series, period: int)

Rolling Maximum

### mdi(prices, period: int = 14)

Minus Directional Index

Args:
    period (int) : time period, default 14

### mfi(prices, period: int = 14)

Money Flow Index 

Args:
    period (int) : time period, default 14

### midprice(prices)

Mid Price

Value of (high + low) / 2

### min(series, period: int)

Rolling Minimum

Args:
    period (int) : time period, required

### natr(prices, period: int = 14)

Average True Range (normalized)

Args:
    period (int) : time period, default 14

### pdi(prices, period: int = 14)

Plus Directional Index

Args:
    period (int) : time period, default 14

### ppo(series, n1: int = 12, n2: int = 26, n3: int = 9)

Price Percentage Oscillator

Args:
    n1 (int) : short time period, default 12
    n2 (int) : long time period, default 26
    n3 (int) : signal time period, default 9

Outputs:
    ppo, pposignal, ppohist

### price(prices, item: str = None)

Generic Price 

Args:
    item (str) : one of 'open', 'high', 'low', 'close',
        'avg', 'mid', 'typ', 'wcl' defaults to 'close'

### qsf(series, period: int = 20, offset: int = 0)

Quadratic Series Forecast (quadratic regression)

Args:
    period (int) : time period, default 20

### rma(series, period: int)

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

### roc(series, period: int = 1)

Rate of Change

Args:
    period (int) : time period, default 1
    when negative the calculation is shifted back

### rsi(series, period: int = 14)

Relative Strength Index

Args:
    period (int) : time period, default 14

### rvalue(series, period: int = 20)

R-Value (linear regression)

Args:
    period (int) : time period, default 20

### sar(prices, afs: float = 0.02, maxaf: float = 0.2)

Parabolic Stop and Reverse

Args:
    afs (float) : starting acceleration factor, default 0.02
    maxaf (float) : maximum acceleration factor, default 0.2

### shift(series, period: int)

Shift Function

Args:
    period (int) : time period, required

### sign(series)

Sign

### slope(series, period: int = 20)

Slope (linear regression)

Args:
    period (int) : time period, default 20

### sma(series, period: int)

Simple Moving Average

Args:
    period (int) : time period, required

### stdev(series, period: int = 20)

Standard Deviation

Args:
    period (int) : time period, default 20

### step(series, threshold: float = 1.0)

Step Function

Limit value changes to threshold (in absolute value)

Args:
    threshold (float) : threshold value, default 1.0

### stoch(prices, period: int = 14, fastn: int = 3, slown: int = 3)

Stochastic Oscillator

Args:
    period (int) :  time period of window, default, 14
    fastn (int) : time period of fast average, default 3
    slown (int) : time period of slow average, default 3

### streak(series)

Consecutive streak of values above zero

### sum(series, period: int)

Rolling sum

Args:
    period (int) : time period, required

### tema(series, period: int = 20)

Triple Exponential Moving Average

Args:
    period (int) : time period, default 20

### trange(prices, *, log_prices: bool = False, percent: bool = False)

True Range

Args:
    log_prices (bool) : whether to apply log to prices before calculation
    percent (bool) : result as percentage of price

### tsf(series, period: int = 20, offset: int = 0)

Time Series Forecast (linear regression)

Args:
    period (int) : time period, default 20

### typprice(prices)

Typical Price

Value of (high + low + close ) / 3

### updown(series, up_level: float = 0.0, down_level: float = 0.0)

Flag for value crossing up & down levels

Args:
    up_level (float) : flag set at 1 above that level
    down_level (float) : flag set at 0 below that level

### wclprice(prices)

Weighted Close Price

Value of (high + low + 2 * close) / 4

### wma(series, period: int)

Weighted Moving Average
    
Args:
    period (int) : time period, required
