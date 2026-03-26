# mintalib.core

Calculation routines implemented in cython.

Routines are typically named `calc_` followed by an indicator name all in lower caps as in `calc_sma`.

The first parameter `series` or `prices` indicates whether the calculation accepts a single series or a prices dataframe.

A `prices` dataframe should contain the columns `open`, `high`, `low`, `close` and optionally `volume` all in **lower case**.

The `wrap` parameter dictates whether to wrap the calculation result to match the type of the inputs.

---

### `calc_abs(series)`

Absolute Value

---

### `calc_adx(prices, period=14)`

Average Directional Index

Args:
    period (int) : time period, default 14

---

### `calc_alma(series, period=9, offset=0.85, sigma=6.0)`

Arnaud Legoux Moving Average

---

### `calc_atr(prices, period=14)`

Average True Range

Args:
    period (int) : time period, default 14    

---

### `calc_avgprice(prices)`

Average Price

Value of (open + high + low + close) / 4

---

### `calc_bbands(prices, period=20, nbdev=2.0)`

Bollinger Bands

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

---

### `calc_bbp(prices, period=20, nbdev=2.0)`

Bollinger Bands Percent (%B)

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

---

### `calc_bbw(prices, period=20, nbdev=2.0)`

Bollinger Bands Width

Args:
    period (int) : time period, default 20
    nbdev (float) : bands width in number of standard deviations

---

### `calc_bop(prices, period=20)`

Balance of Power

Args:
    period (int) : time period, default 20

---

### `calc_cci(prices, period=20)`

Commodity Channel Index

Args:
    period (int) : time period, default 20

---

### `calc_clag(series, period=1)`

Confirmation Lag

Changes value only after a confirmation period 

Args:
    period (int) : time period, default 1

---

### `calc_cmf(prices, period=20)`

Chaikin Money Flow

Args:
    period (int) : time period, default 20

---

### `calc_crossover(series, level=0.0)`

Cross Over

Yields a value of 1 at the point where series crosses over level

Args:
    level (float) : level to cross, default 0.0

---

### `calc_crossunder(series, level=0.0)`

Cross Under

Yields a value of 1 at the point where series crosses under level

Args:
    level (float) : level to cross, default 0.0

---

### `calc_curve(series, period=20)`

Curve (quadratic regression) 

---

### `calc_dema(series, period)`

Double Exponential Moving Average

Args:
    period (int) : time period, required    

---

### `calc_diff(series, period=1)`

Difference

Difference between current value and the one offset by period

Args:
    period (int) : time period, default 1

---

### `calc_dmi(prices, period=14)`

Directional Movement Indicator

Args:
    period (int) : time period, default 14

---

### `calc_ema(series, period, *, adjust=False)`

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

---

### `calc_eval(prices, expr, *, as_flag=False)`

Expression Eval (pandas only)

Args:
    expr (str) : expression to eval

---

### `calc_exp(series)`

Exponential

---

### `calc_flag(series)`

Flag Value

Flag value of 1 for positive, 0 for zero or negative, and NaN otherwize

---

### `calc_hma(series, period)`

Hull Moving Average

Args:
    period (int) : time period, required    

---

### `calc_kama(series, period=10, fastn=2, slown=30)`

Kaufman Adaptive Moving Average

Args:
    period (int) : time period for efficiency ratio, default 10
    fastn (int) : time period for fast moving average, default, 2
    slown (int) : time period for slow moving average, default 30

---

### `calc_keltner(prices, period=20, nbatr=2.0)`

Keltner Channel

Args:
    period (int) : time period, default 20
    nbatr (float) : channel width in number of atrs, default 2.0

---

### `calc_ker(series, period=10)`

Kaufman Efficiency Ratio

Args:
    period (int) : time period, default 10

---

### `calc_lag(series, period)`

Lag Function

Args:
    period (int) : time period, required

---

### `calc_log(series)`

Logarithm 

---

### `calc_lroc(series, period=1)`

Logarithmic Rate of Change

Equivalent to the difference of log values

Args:
    period (int) : time period, default 1
    when negative the calculation is shifted back

---

### `calc_macd(series, n1=12, n2=26, n3=9)`

Moving Average Convergence Divergence

Args:
    n1 (int) : show time period, default 12
    n2 (int) : long time periodm, default 26
    n3 (int) : signal time period, default 9  

Outputs:
    macd, macdsignal, macdhist

---

### `calc_macdv(prices, n1=12, n2=26, n3=9)`

Moving Average Convergence Divergence - Volatility Normalized

Args:
    n1 (int) : show time period, default 12
    n2 (int) : long time periodm, default 26
    n3 (int) : signal time period, default 9  

Outputs:
    macdv, macdvsignal, macdvhist

---

### `calc_mad(series, period: 'int' = 14)`

Rolling Mean Absolute Deviation

---

### `calc_mav(series, period=20, *, ma_type='SMA')`

Generic Moving Average

Moving average computed according to ma_type

Args:
    ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
            defaults to 'SMA'

---

### `calc_max(series, period)`

Rolling Maximum 

---

### `calc_mdi(prices, period=14)`

Minus Directional Index

Args:
    period (int) : time period, default 14

---

### `calc_mfi(prices, period=14)`

Money Flow Index 

Args:
    period (int) : time period, default 14

---

### `calc_midprice(prices)`

Mid Price

Value of (high + low) / 2

---

### `calc_min(series, period)`

Rolling Minimum

Args:
    period (int) : time period, required

---

### `calc_natr(prices, period=14)`

Average True Range (normalized)

Args:
    period (int) : time period, default 14    

---

### `calc_pdi(prices, period=14)`

Plus Directional Index

Args:
    period (int) : time period, default 14

---

### `calc_ppo(series, n1=12, n2=26, n3=9)`

Price Percentage Oscillator

Args:
    n1 (int) : short time period, default 12
    n2 (int) : long time period, default 26
    n3 (int) : signal time period, default 9

Outputs:
    ppo, pposignal, ppohist

---

### `calc_price(prices, item: 'str' = None)`

Generic Price 

Args:
    item (str) : one of 'open', 'high', 'low', 'close',
        'avg', 'mid', 'typ', 'wcl' defaults to 'close'

---

### `calc_qsf(series, period=20, offset=0)`

Quadratic Series Forecast (quadratic regression)

Args:
    period (int) : time period, default 20

---

### `calc_rma(series, period)`

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

---

### `calc_roc(series, period=1)`

Rate of Change

Args:
    period (int) : time period, default 1
    when negative the calculation is shifted back

---

### `calc_rsi(series, period=14)`

Relative Strength Index

Args:
    period (int) : time period, default 14

---

### `calc_rvalue(series, period=20)`

R-Value (linear regression)

Args:
    period (int) : time period, default 20

---

### `calc_sar(prices, afs=0.02, maxaf=0.2)`

Parabolic Stop and Reverse

Args:
    afs (float) : starting acceleration factor, default 0.02
    maxaf (float) : maximum acceleration factor, default 0.2

---

### `calc_shift(series, period)`

Shift Function

Args:
    period (int) : time period, required

---

### `calc_sign(series)`

Sign

---

### `calc_slope(series, period=20)`

Slope (linear regression)

Args:
    period (int) : time period, default 20

---

### `calc_sma(series, period)`

Simple Moving Average

Args:
    period (int) : time period, required

---

### `calc_stdev(series, period=20)`

Standard Deviation

Args:
    period (int) : time period, default 20

---

### `calc_step(series, threshold: 'float' = 1.0)`

Step Function

Limit value changes to threshold (in absolute value)

Args:
    threshold (float) : threshold value, default 1.0

---

### `calc_stoch(prices, period=14, fastn=3, slown=3)`

Stochastic Oscillator

Args:
    period (int) :  time period of window, default, 14
    fastn (int) : time period of fast average, default 3
    slown (int) : time period of slow average, default 3

---

### `calc_streak(series)`

Consecutive streak of values above zero

---

### `calc_sum(series, period)`

Rolling sum

Args:
    period (int) : time period, required

---

### `calc_tema(series, period=20)`

Triple Exponential Moving Average

Args:
    period (int) : time period, default 20

---

### `calc_trange(prices, *, log_prices=False, percent=False)`

True Range

Args:
    log_prices (bool) : whether to apply log to prices before calculation
    percent (bool) : result as percentage of price

---

### `calc_tsf(series, period=20, offset=0)`

Time Series Forecast (linear regression)

Args:
    period (int) : time period, default 20

---

### `calc_typprice(prices)`

Typical Price

Value of (high + low + close ) / 3

---

### `calc_updown(series, up_level=0.0, down_level=0.0)`

Flag for value crossing up & down levels

Args:
    up_level (float) : flag set at 1 above that level
    down_level (float) : flag set at 0 below that level

---

### `calc_wclprice(prices)`

Weighted Close Price

Value of (high + low + 2 * close) / 4

---

### `calc_wma(series, period)`

Weighted Moving Average
    
Args:
    period (int) : time period, required
