# mintalib.indicators

Indicators offer a composable interface where a calculation routine is bound with its parameters.

This module is pandas-only: indicators accept pandas DataFrames, pandas Series, or numpy arrays,
and return pandas results. For polars, use `mintalib.expressions`.

An indicator instance is a callable applied to prices or series data: `SMA(50)(prices)`.

Indicators chain via the `|` operator or the equivalent `.then()` method:
`EMA(20) | ROC(1)` is the same as `EMA(20).then(ROC(1))`. The fluent form is handy in longer chains: `EMA(20).then(ROC(1)).as_expr()`.

Single-output indicators return a pandas Series; multi-output indicators (e.g. `MACD`, `BBANDS`) return a DataFrame.
Select one output of a multi-output indicator as a series indicator with `MACD()["macd"]`.

---

### ABS

`ABS(*, item: str | None = None)`

Absolute Value

### ADX

`ADX(period: int = 14)`

Average Directional Index


**Arguments:**
 - **period (int):**  time period, default 14



### ALMA

`ALMA(period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, item: str | None = None)`

Arnaud Legoux Moving Average

### ATR

`ATR(period: int = 14)`

Average True Range


**Arguments:**
 - **period (int):**  time period, default 14



### AVGPRICE

`AVGPRICE()`

Average Price

Value of (open + high + low + close) / 4

### BBANDS

`BBANDS(period: int = 20, nbdev: float = 2.0, *, item: str | None = None)`

Bollinger Bands


**Arguments:**
 - **period (int):**  time period, default 20
 - **nbdev (float):**  bands width in number of standard deviations



### BBP

`BBP(period: int = 20, nbdev: float = 2.0, *, item: str | None = None)`

Bollinger Bands Percent (%B)


**Arguments:**
 - **period (int):**  time period, default 20
 - **nbdev (float):**  bands width in number of standard deviations



### BBW

`BBW(period: int = 20, nbdev: float = 2.0, *, item: str | None = None)`

Bollinger Bands Width


**Arguments:**
 - **period (int):**  time period, default 20
 - **nbdev (float):**  bands width in number of standard deviations



### BOP

`BOP(period: int = 20)`

Balance of Power


**Arguments:**
 - **period (int):**  time period, default 20



### CCI

`CCI(period: int = 20)`

Commodity Channel Index


**Arguments:**
 - **period (int):**  time period, default 20



### CLAG

`CLAG(period: int = 1, *, item: str | None = None)`

Confirmation Lag

Changes value only after a confirmation period 


**Arguments:**
 - **period (int):**  time period, default 1



### CMF

`CMF(period: int = 20)`

Chaikin Money Flow


**Arguments:**
 - **period (int):**  time period, default 20



### CROSSOVER

`CROSSOVER(level: float = 0.0, *, item: str | None = None)`

Cross Over

Yields a value of 1 at the point where series crosses over level


**Arguments:**
 - **level (float):**  level to cross, default 0.0



### CROSSUNDER

`CROSSUNDER(level: float = 0.0, *, item: str | None = None)`

Cross Under

Yields a value of 1 at the point where series crosses under level


**Arguments:**
 - **level (float):**  level to cross, default 0.0



### DEMA

`DEMA(period: int, *, item: str | None = None)`

Double Exponential Moving Average


**Arguments:**
 - **period (int):**  time period, required



### DIFF

`DIFF(period: int = 1, *, item: str | None = None)`

Difference

Difference between current value and the one offset by period


**Arguments:**
 - **period (int):**  time period, default 1



### DMI

`DMI(period: int = 14)`

Directional Movement Indicator


**Arguments:**
 - **period (int):**  time period, default 14



### DONCHIAN

`DONCHIAN(period: int = 20)`

Donchian Channel


**Arguments:**
 - **period (int):**  time period, default 20



### EMA

`EMA(period: int, *, adjust: bool = False, item: str | None = None)`

Exponential Moving Average


**Arguments:**
 - **period (int):**  time period, required
 - **adjust (bool):**  whether to adjust weights, default False
   when true update ratio increases gradually (see formula)



**Formula:**
> EMA is calculated as a recursive formula
> The standard formula is ema += alpha * (value - ema)
>     with alpha = 2.0 / (period + 1.0)
> The adjusted formula is ema = num/div
>     where num = value + rho * num, div = 1.0 + rho * div
>     with rho = 1.0 - alpha


### EVAL

Evaluate a pandas expression against a DataFrame's columns.

### EXP

`EXP(*, item: str | None = None)`

Exponential

### FLAG

`FLAG(*, item: str | None = None)`

Flag Value

Flag value of 1 for positive, 0 for zero or negative, and NaN otherwize

### HMA

`HMA(period: int, *, item: str | None = None)`

Hull Moving Average


**Arguments:**
 - **period (int):**  time period, required



### KAMA

`KAMA(period: int = 10, fastn: int = 2, slown: int = 30, *, item: str | None = None)`

Kaufman Adaptive Moving Average


**Arguments:**
 - **period (int):**  time period for efficiency ratio, default 10
 - **fastn (int):**  time period for fast moving average, default, 2
 - **slown (int):**  time period for slow moving average, default 30



### KELTNER

`KELTNER(period: int = 20, nbatr: float = 2.0)`

Keltner Channel


**Arguments:**
 - **period (int):**  time period, default 20
 - **nbatr (float):**  channel width in number of atrs, default 2.0



### KER

`KER(period: int = 10, *, item: str | None = None)`

Kaufman Efficiency Ratio


**Arguments:**
 - **period (int):**  time period, default 10



### LAG

`LAG(period: int, *, item: str | None = None)`

Lag Function


**Arguments:**
 - **period (int):**  time period, required



### LINREG

`LINREG(period: int = 20, offset: int = 0, *, item: str | None = None)`

Linear Regression (least squares moving average)

Value of the regression line at the current bar,
with `offset` projecting the line forward.


**Arguments:**
 - **period (int):**  time period, default 20
 - **offset (int):**  forecast offset, default 0



### LINREG_RMSE

`LINREG_RMSE(period: int = 20, *, item: str | None = None)`

Linear Regression Root Mean Square Error


**Arguments:**
 - **period (int):**  time period, default 20



### LINREG_RVALUE

`LINREG_RVALUE(period: int = 20, *, item: str | None = None)`

Linear Regression R-Value


**Arguments:**
 - **period (int):**  time period, default 20



### LINREG_SLOPE

`LINREG_SLOPE(period: int = 20, *, item: str | None = None)`

Linear Regression Slope


**Arguments:**
 - **period (int):**  time period, default 20



### LOG

`LOG(*, item: str | None = None)`

Logarithm

### LROC

`LROC(period: int = 1, *, item: str | None = None)`

Logarithmic Rate of Change

Equivalent to the difference of log values


**Arguments:**
 - **period (int):**  time period, default 1
 - when negative the calculation is shifted back



### MACD

`MACD(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str | None = None)`

Moving Average Convergence Divergence


**Arguments:**
 - **n1 (int):**  short time period, default 12
 - **n2 (int):**  long time period, default 26
 - **n3 (int):**  signal time period, default 9  



**Outputs:**
> macd, macdsignal, macdhist


### MACDV

`MACDV(n1: int = 12, n2: int = 26, n3: int = 9)`

Moving Average Convergence Divergence - Volatility Normalized


**Arguments:**
 - **n1 (int):**  short time period, default 12
 - **n2 (int):**  long time period, default 26
 - **n3 (int):**  signal time period, default 9  



**Outputs:**
> macdv, macdvsignal, macdvhist


### MAD

`MAD(period: int = 14, *, item: str | None = None)`

Rolling Mean Absolute Deviation

### MAV

`MAV(period: int = 20, *, ma_type: str = 'SMA', item: str | None = None)`

Generic Moving Average

Moving average computed according to ma_type


**Arguments:**
 - **ma_type (str):**  one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
   defaults to 'SMA'



### MAX

`MAX(period: int, *, item: str | None = None)`

Rolling Maximum

### MDI

`MDI(period: int = 14)`

Minus Directional Index


**Arguments:**
 - **period (int):**  time period, default 14



### MEDPRICE

`MEDPRICE()`

Median Price

Value of (high + low) / 2

### MFI

`MFI(period: int = 14)`

Money Flow Index


**Arguments:**
 - **period (int):**  time period, default 14



### MIN

`MIN(period: int, *, item: str | None = None)`

Rolling Minimum


**Arguments:**
 - **period (int):**  time period, required



### NATR

`NATR(period: int = 14)`

Normalized Average True Range


**Arguments:**
 - **period (int):**  time period, default 14



### PDI

`PDI(period: int = 14)`

Plus Directional Index


**Arguments:**
 - **period (int):**  time period, default 14



### PPO

`PPO(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str | None = None)`

Price Percentage Oscillator


**Arguments:**
 - **n1 (int):**  short time period, default 12
 - **n2 (int):**  long time period, default 26
 - **n3 (int):**  signal time period, default 9



**Outputs:**
> ppo, pposignal, ppohist


### PRICE

`PRICE(item: str | None = None)`

Generic Price


**Arguments:**
 - **item (str):**  price type, one of:
   'open', 'high', 'low', 'close' (default),
   'avg' or 'ohlc4'  — average price (open + high + low + close) / 4,
   'med' or 'hl2'    — median price (high + low) / 2,
   'typ' or 'hlc3'   — typical price (high + low + close) / 3,
   'wcl' or 'hlcc4'  — weighted close (high + low + 2 * close) / 4



### QUADREG

`QUADREG(period: int = 20, offset: int = 0, *, item: str | None = None)`

Quadratic Regression (parabolic moving average)

Value of the regression parabola at the current bar,
with `offset` projecting the parabola forward.


**Arguments:**
 - **period (int):**  time period, default 20
 - **offset (int):**  forecast offset, default 0



### QUADREG_CURVE

`QUADREG_CURVE(period: int = 20, *, item: str | None = None)`

Quadratic Regression Curve


**Arguments:**
 - **period (int):**  time period, default 20



### QUADREG_RMSE

`QUADREG_RMSE(period: int = 20, *, item: str | None = None)`

Quadratic Regression Root Mean Square Error


**Arguments:**
 - **period (int):**  time period, default 20



### QUADREG_RVALUE

`QUADREG_RVALUE(period: int = 20, *, item: str | None = None)`

Quadratic Regression R-Value

Partial correlation of the quadratic term, given the linear term.


**Arguments:**
 - **period (int):**  time period, default 20



### QUADREG_SLOPE

`QUADREG_SLOPE(period: int = 20, offset: int = 0, *, item: str | None = None)`

Quadratic Regression Slope

Slope of the regression parabola at the current bar,
with `offset` projecting the slope forward.


**Arguments:**
 - **period (int):**  time period, default 20
 - **offset (int):**  forecast offset, default 0



### RMA

`RMA(period: int, *, item: str | None = None)`

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

### ROC

`ROC(period: int = 1, *, item: str | None = None)`

Rate of Change


**Arguments:**
 - **period (int):**  time period, default 1
 - when negative the calculation is shifted back



### RSI

`RSI(period: int = 14, *, item: str | None = None)`

Relative Strength Index


**Arguments:**
 - **period (int):**  time period, default 14



### SAR

`SAR(afs: float = 0.02, maxaf: float = 0.2)`

Parabolic Stop and Reverse


**Arguments:**
 - **afs (float):**  starting acceleration factor, default 0.02
 - **maxaf (float):**  maximum acceleration factor, default 0.2



### SIGN

`SIGN(*, item: str | None = None)`

Sign

### SMA

`SMA(period: int, *, item: str | None = None)`

Simple Moving Average


**Arguments:**
 - **period (int):**  time period, required



### STDEV

`STDEV(period: int = 20, *, item: str | None = None)`

Standard Deviation


**Arguments:**
 - **period (int):**  time period, default 20



### STEP

`STEP(threshold: float = 1.0, *, item: str | None = None)`

Step Function

Limit value changes to threshold (in absolute value)


**Arguments:**
 - **threshold (float):**  threshold value, default 1.0



### STOCH

`STOCH(period: int = 14, fastn: int = 3, slown: int = 3)`

Stochastic Oscillator


**Arguments:**
 - **period (int):**   time period of window, default, 14
 - **fastn (int):**  time period of fast average, default 3
 - **slown (int):**  time period of slow average, default 3



### STREAK

`STREAK(*, item: str | None = None)`

Consecutive streak of values above zero

### SUM

`SUM(period: int, *, item: str | None = None)`

Rolling sum


**Arguments:**
 - **period (int):**  time period, required



### TEMA

`TEMA(period: int = 20, *, item: str | None = None)`

Triple Exponential Moving Average


**Arguments:**
 - **period (int):**  time period, default 20



### TRANGE

`TRANGE(*, log_prices: bool = False, percent: bool = False)`

True Range


**Arguments:**
 - **log_prices (bool):**  whether to apply log to prices before calculation
 - **percent (bool):**  result as percentage of price



### TYPPRICE

`TYPPRICE()`

Typical Price

Value of (high + low + close ) / 3

### UPDOWN

`UPDOWN(up_level: float = 0.0, down_level: float = 0.0, *, item: str | None = None)`

Flag for value crossing up & down levels


**Arguments:**
 - **up_level (float):**  flag set at 1 above that level
 - **down_level (float):**  flag set at 0 below that level



### WCLPRICE

`WCLPRICE()`

Weighted Close Price

Value of (high + low + 2 * close) / 4

### WMA

`WMA(period: int, *, item: str | None = None)`

Weighted Moving Average
    

**Arguments:**
 - **period (int):**  time period, required



### ZLEMA

`ZLEMA(period: int, *, item: str | None = None)`

Zero-Lag Exponential Moving Average


**Arguments:**
 - **period (int):**  time period, required



**Formula:**
> ZLEMA is an EMA applied to a de-lagged series
> data = 2 * value - value[lag] with lag = (period - 1) // 2

