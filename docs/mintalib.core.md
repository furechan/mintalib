# `mintalib.core` module

Calculation routines implemented in cython.

Routines are typically named `calc_` followed by an indicator name all in lower caps as in `calc_sma`.

The first parameter `series` or `prices` indicates whether the calculation accepts a single series or a prices dataframe.

A `prices` dataframe should contain the columns `open`, `high`, `low`, `close` and optionally `volume` all in **lower case**.

The `wrap` parameter dictates whether to wrap the calculation result to match the type of the inputs.


## `check_size` function

```python
check_size(*args)
```

check all series have the same size and return the size
## `column_accessor` function

```python
column_accessor(data)
```

column accessor if applicable
## `get_series` function

```python
get_series(data, item: str = None, *, default_item: str = 'close')
```

get series from prices or series data
## `with_metadata` function

```python
with_metadata(*, same_scale: bool = None)
```

update function with metadata
## `wrap_function` function

```python
wrap_function(source)
```

decorator to update function with documentation from source
## `wrap_indicator` function

```python
wrap_indicator(source)
```

decorator to update indicator with documentation from source
## `wrap_result` function

```python
wrap_result(result, source, name: str = None)
```

wrap result to match source data type
## `calc_price` function

```python
calc_price(prices, item: str = None, *, wrap: bool = False)
```

Generic Price 
   
   Args:
- item (str) : one of 'open', 'high', 'low', 'close',
           'avg', 'mid', 'typ', 'wcl' defaults to 'close'

## `calc_avgprice` function

```python
calc_avgprice(prices, *, wrap: bool = False)
```

Average Price

Value of (open + high + low + close) / 4

## `calc_typprice` function

```python
calc_typprice(prices, *, wrap: bool = False)
```

Typical Price

Value of (high + low + close ) / 3

## `calc_wclprice` function

```python
calc_wclprice(prices, *, wrap: bool = False)
```

Weighted Close Price

Value of (high + low + 2 * close) / 4

## `calc_midprice` function

```python
calc_midprice(prices, *, wrap: bool = False)
```

Mid Price

Value of (high + low) / 2

## `calc_crossover` function

```python
calc_crossover(series, level: float = 0.0, *, wrap: bool = False)
```

Cross Over

Yields a value of 1 at the point where series crosses over level

Args:
- level (float) : level to cross, default 0.0

## `calc_crossunder` function

```python
calc_crossunder(series, level: float = 0.0, *, wrap: bool = False)
```

Cross Under

Yields a value of 1 at the point where series crosses under level

Args:
- level (float) : level to cross, default 0.0

## `calc_flag` function

```python
calc_flag(series, *, wrap: bool = False)
```

Flag Value

Flag value of 1 for positive, 0 for zero or negative, and NaN for missing values

Args:
- expr (str) : expression to evaluate (optional) (pandas only!)

## `calc_updown` function

```python
calc_updown(series, up_level: float = 0.0, down_level: float = 0.0, *, wrap: bool = False)
```

Flag for value crossing up & down levels

Args:
- up_level (float) : flag set at 1 above that level
- down_level (float) : flag set at 0 below that level

## `where_flag` function

```python
where_flag(flag, x, y, z: float = nan, *, wrap: bool = False)
```

Value according to flag
## `calc_sign` function

```python
calc_sign(series, na_value: float = nan, *, wrap: bool = False)
```

Sign
## `calc_step` function

```python
calc_step(series, threshold: float = 1.0, *, wrap: bool = False)
```

Step Function

Limit value changes to threshold (in absolute value)

Args:
- threshold (float) : threshold value, default 1.0

## `calc_clag` function

```python
calc_clag(series, period: int = 1, *, wrap: bool = False)
```

Confirmation Lag

Changes value only after a confirmation period 

Args:
- period (int) : time period, default 1

## `calc_abs` function

```python
calc_abs(series, *, wrap: bool = False)
```

Absolute Value
## `calc_log` function

```python
calc_log(series, *, wrap: bool = False)
```

Logarithm
## `calc_exp` function

```python
calc_exp(series, *, wrap: bool = False)
```

Exponential
## `calc_shift` function

```python
calc_shift(series, period: int, *, wrap: bool = False)
```

Shift Function

Args:
- period (int) : time period, required

## `calc_diff` function

```python
calc_diff(series, period: int = 1, *, wrap: bool = False)
```

Difference

Difference between current value and the one offset by period

Args:
- period (int) : time period, default 1

## `calc_lag` function

```python
calc_lag(series, period: int, *, wrap: bool = False)
```

Lag Function

Args:
- period (int) : time period, required

## `calc_min` function

```python
calc_min(series, period: int, *, wrap: bool = False)
```

Rolling Minimum

Args:
- period (int) : time period, required

## `calc_max` function

```python
calc_max(series, period: int, *, wrap: bool = False)
```

Rolling Maximum
## `calc_sum` function

```python
calc_sum(series, period: int, *, wrap: bool = False)
```

Rolling sum

Args:
- period (int) : time period, required

## `calc_roc` function

```python
calc_roc(series, period: int = 1, *, wrap: bool = False)
```

Rate of Change

Args:
- period (int) : time period, default 1
    when negative the calculation is shifted back

## `calc_lroc` function

```python
calc_lroc(series, period: int = 1, *, wrap: bool = False)
```

Logarithmic Rate of Change

Equivalent to the difference of log values

Args:
- period (int) : time period, default 1
    when negative the calculation is shifted back

## `calc_mad` function

```python
calc_mad(series, period: int = 14, *, wrap: bool = False)
```

Rolling Mean Absolute Deviation
## `calc_stdev` function

```python
calc_stdev(series, period: int = 20, *, wrap: bool = False)
```

Standard Deviation

Args:
- period (int) : time period, default 20

## `calc_mav` function

```python
calc_mav(series, period: int = 20, *, ma_type: str = 'SMA', wrap: bool = False)
```

Generic Moving Average

Moving average computed according to ma_type

Args:
- ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
            defaults to 'SMA'

## `calc_sma` function

```python
calc_sma(series, period: int, *, wrap: bool = False)
```

Simple Moving Average

Args:
- period (int) : time period, required

## `calc_ema` function

```python
calc_ema(series, period: int, *, adjust: bool = False, wrap: bool = False)
```

Exponential Moving Average

Args:
- period (int) : time period, required
- adjust (bool) : whether to adjust weights, default False
        when true update ratio increases gradually (see formula)

Formula:
+ EMA is calculated as a recursive formula
    The standard formula is ema += alpha * (value - ema)
        with alpha = 2.0 / (period + 1.0)
    The adjusted formula is ema = num/div
        where num = value + rho * num, div = 1.0 + rho * div
        with rho = 1.0 - alpha

## `calc_rma` function

```python
calc_rma(series, period: int, *, wrap: bool = False)
```

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

## `calc_wma` function

```python
calc_wma(series, period: int, *, wrap: bool = False)
```

Weighted Moving Average
    
Args:
- period (int) : time period, required

## `calc_hma` function

```python
calc_hma(series, period: int, *, wrap: bool = False)
```

Hull Moving Average

Args:
- period (int) : time period, required    

## `calc_dema` function

```python
calc_dema(series, period: int, *, wrap: bool = False)
```

Double Exponential Moving Average
 
Args:
- period (int) : time period, required    

## `calc_tema` function

```python
calc_tema(series, period: int = 20, *, wrap: bool = False)
```

Triple Exponential Moving Average

Args:
- period (int) : time period, default 20

## `calc_alma` function

```python
calc_alma(series, period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, wrap: bool = False)
```

Arnaud Legoux Moving Average
## `calc_rsi` function

```python
calc_rsi(series, period: int = 14, *, wrap: bool = False)
```

Relative Strength Index

Args:
- period (int) : time period, default 14

## `calc_dmi` function

```python
calc_dmi(prices, period: int = 14, *, wrap: bool = False)
```

Directional Movement Indicator

Args:
- period (int) : time period, default 14

## `calc_adx` function

```python
calc_adx(prices, period: int = 14, *, wrap: bool = False)
```

Average Directional Index

Args:
- period (int) : time period, default 14

## `calc_pdi` function

```python
calc_pdi(prices, period: int = 14, *, wrap: bool = False)
```

Plus Directional Index

Args:
- period (int) : time period, default 14

## `calc_mdi` function

```python
calc_mdi(prices, period: int = 14, *, wrap: bool = False)
```

Minus Directional Index

Args:
- period (int) : time period, default 14

## `calc_trange` function

```python
calc_trange(prices, *, log_prices: bool = False, percent: bool = False, wrap: bool = False)
```

True Range

Args:
- log_percent (bool) : whether to apply log to prices before calculatio
- percent (bool) : result as percentage of price

## `calc_atr` function

```python
calc_atr(prices, period: int = 14, *, wrap: bool = False)
```

Average True Range

Args:
- period (int) : time period, default 14    

## `calc_natr` function

```python
calc_natr(prices, period: int = 14, *, wrap: bool = False)
```

Average True Range (normalized)

Args:
- period (int) : time period, default 14    

## `calc_sar` function

```python
calc_sar(prices, afs: float = 0.02, maxaf: float = 0.2, *, wrap: bool = False)
```

Parabolic Stop and Reverse

Args:
- afs (float) : starting acceleration factor, default 0.02
- maxaf (float) : maximum acceleration factor, default 0.2

## `calc_cci` function

```python
calc_cci(prices, period: int = 20, *, wrap: bool = False)
```

Commodity Channel Index

Args:
- period (int) : time period, default 20

## `calc_cmf` function

```python
calc_cmf(prices, period: int = 20, *, wrap: bool = False)
```

Chaikin Money Flow

Args:
- period (int) : time period, default 20

## `calc_mfi` function

```python
calc_mfi(prices, period: int = 14, *, wrap: bool = False)
```

Money Flow Index 

Args:
- period (int) : time period, default 14

## `calc_bop` function

```python
calc_bop(prices, period: int = 20, *, wrap: bool = False)
```

Balance of Power

Args:
- period (int) : time period, default 20

## `calc_bbands` function

```python
calc_bbands(prices, period: int = 20, nbdev: float = 2.0, *, wrap: bool = False)
```

Bollinger Bands

Args:
- period (int) : time period, default 20
- nbdev (float) : bands width in number of standard deviations

## `calc_keltner` function

```python
calc_keltner(prices, period: int = 20, nbatr: float = 2.0, *, wrap: bool = False)
```

Keltner Channel

Args:
- period (int) : time period, default 20
- nbatr (float) : channel width in number of atrs, default 2.0

## `calc_ker` function

```python
calc_ker(series, period: int = 10, *, wrap: bool = False)
```

Kaufman Efficiency Ratio

Args:
- period (int) : time period, default 10

## `calc_kama` function

```python
calc_kama(series, period: int = 10, fastn: int = 2, slown: int = 30, *, wrap: bool = False)
```

Kaufman Adaptive Moving Average

Args:
- period (int) : time period for efficiency ratio, default 10
- fastn (int) : time period for fast moving average, default, 2
- slown (int) : time period for slow moving average, default 30

## `calc_macd` function

```python
calc_macd(series, n1: int = 12, n2: int = 26, n3: int = 9, *, wrap: bool = False)
```

Moving Average Convergenge Divergence

Args:
- n1 (int) : show time period, default 12
- n2 (int) : long time periodm, default 26
- n3 (int) : signal time period, default 9  

Outputs:
+ macd, macdsignal, macdhist

## `calc_ppo` function

```python
calc_ppo(series, n1: int = 12, n2: int = 26, n3: int = 9, *, wrap: bool = False)
```

Price Percentage Oscillator

Args:
- n1 (int) : short time period, default 12
- n2 (int) : long time period, default 26
- n3 (int) : signal time period, default 9

Outputs:
+ ppo, pposignal, ppohist

## `linear_regression` function

```python
linear_regression(series, period: int = 20, *, option: int = 0, offset: int = 0, wrap: bool = False)
```

Linear Regression

Args:
- period (int) : time period, default 20

## `calc_slope` function

```python
calc_slope(series, period: int = 20, *, wrap: bool = False)
```

Slope (linear regression)

Args:
- period (int) : time period, default 20

## `calc_rvalue` function

```python
calc_rvalue(series, period: int = 20, *, wrap: bool = False)
```

R-Value (linear regression)

Args:
- period (int) : time period, default 20

## `calc_tsf` function

```python
calc_tsf(series, period: int = 20, offset: int = 0, *, wrap: bool = False)
```

Time Series Forecast (linear regression)

Args:
- period (int) : time period, default 20

## `quadratic_regression` function

```python
quadratic_regression(series, period: int = 20, *, option: int = 0, wrap: bool = False)
```

Curve (quadratic regression)
## `calc_curve` function

```python
calc_curve(series, period: int = 20, *, wrap: bool = False)
```

Curve (quadratic regression)
## `calc_stoch` function

```python
calc_stoch(prices, period: int = 14, fastn: int = 3, slown: int = 3, *, wrap: bool = False)
```

Stochastic Oscillator

Args:
- period (int) :  time period of window, default, 14
- fastn (int) : time period of fast average, default 3
- slown (int) : time period of slow average, default 3

## `calc_streak` function

```python
calc_streak(series, *, wrap: bool = False)
```

Consecutive streak of ups or downs

Length of streak of values all up or down, times +1 or -1 whether ups or downs.

## `calc_eval` function

```python
calc_eval(prices, expr: str, *, as_flag: bool = False, wrap: bool = False)
```

Expression Eval (pandas only)

Args:
- expr (str) : expression to eval

