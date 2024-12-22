# mintalib.core module

Mintalib Core

Calculation routines implemented in cython.

Routines are typically named `calc_` followed by an indicator name all in lower caps as in `calc_sma`.

The first parameter `series` or `prices` indicates whether the calculation accepts a single series or a prices dataframe.

A `prices` dataframe should contain the columns `open`, `high`, `low`, `close` and optionally `volume` all in **lower case**.

The `wrap` parameter dictates whether to wrap the calculation result to match the type of the inputs.
When set to True, pandas inputs will yield a pandas output with an identical index.


## calc_adx function

```python
calc_adx(prices, period=14, *, wrap: bool = False)
```

Average Directional Index

Args:
- period (int) : time period, default 14

## calc_atr function

```python
calc_atr(prices, period=14, *, wrap: bool = False)
```

Average True Range

Args:
- period (int) : time period, default 14    

## calc_avgprice function

```python
calc_avgprice(prices, *, wrap: bool = False)
```

Average Price

Value of (open + high + low + close) / 4

## calc_bbands function

```python
calc_bbands(prices, period=20, nbdev=2.0, *, wrap: bool = False)
```

Bollinger Bands

Args:
- period (int) : time period, default 20
- nbdev (float) : bands width in number of standard deviations

## calc_bop function

```python
calc_bop(prices, period=20, *, wrap: bool = False)
```

Balance of Power

Args:
- period (int) : time period, default 20

## calc_cci function

```python
calc_cci(prices, period=20, *, wrap: bool = False)
```

Commodity Channel Index

Args:
- period (int) : time period, default 20

## calc_cmf function

```python
calc_cmf(prices, period=20, *, wrap: bool = False)
```

Chaikin Money Flow

Args:
- period (int) : time period, default 20

## calc_curve function

```python
calc_curve(series, period=20, *, option=0, offset=0, wrap: bool = False)
```

Curve (time curvilinear regression)
## calc_dema function

```python
calc_dema(series, period, wrap: bool = False)
```

Double Exponential Moving Average
 
Args:
- period (int) : time period, required    

## calc_diff function

```python
calc_diff(series, period=1, *, wrap: bool = False)
```

Difference

Difference between current value and the one offset by period

Args:
- period (int) : time period, default 1

## calc_dmi function

```python
calc_dmi(prices, period=14, *, wrap: bool = False)
```

Directional Movement Indicator

Args:
- period (int) : time period, default 14

## calc_ema function

```python
calc_ema(series, period, *, adjust=False, wrap: bool = False)
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

## calc_eval function

```python
calc_eval(prices, expr: str)
```

Expression Eval (pandas only)

Args:
- expr (str) : expression to eval

## calc_exp function

```python
calc_exp(series, *, wrap: bool = False)
```

Exponential
## calc_flag function

```python
calc_flag(series, *, wrap: bool = False)
```

Flag for value above zero

## calc_hma function

```python
calc_hma(series, period, *, wrap: bool = False)
```

Hull Moving Average

Args:
- period (int) : time period, required    

## calc_kama function

```python
calc_kama(series, period=10, fastn=2, slown=30, *, wrap: bool = False)
```

Kaufman Adaptive Moving Average

Args:
- period (int) : time period for efficiency ratio, default 10
- fastn (int) : time period for fast moving average, default, 2
- slown (int) : time period for slow moving average, default 30

## calc_keltner function

```python
calc_keltner(prices, period=20, nbatr=2.0, *, wrap: bool = False)
```

Keltner Channel

Args:
- period (int) : time period, default 20
- nbatr (float) : channel width in number of atrs, default 2.0

## calc_ker function

```python
calc_ker(series, period=10, *, wrap: bool = False)
```

Kaufman Efficiency Ratio

Args:
- period (int) : time period, default 10

## calc_lag function

```python
calc_lag(series, period, *, wrap: bool = False)
```

Lag Function

Args:
- period (int) : time period, required

## calc_log function

```python
calc_log(series, *, wrap: bool = False)
```

Logarithm
## calc_ma function

```python
calc_ma(series, period=20, *, ma_type: str = None, wrap: bool = False)
```

Generic Moving Average

Moving average computed according to ma_type

Args:
- ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
            defaults to 'SMA'

## calc_macd function

```python
calc_macd(series, n1=12, n2=26, n3=9, wrap: bool = False)
```

Moving Average Convergenge Divergence

Args:
- n1 (int) : show time period, default 12
- n2 (int) : long time periodm, default 26
- n3 (int) : signal time period, default 9  

Outputs:
+ macd, macdsignal, macdhist

## calc_mad function

```python
calc_mad(series, period=20, *, wrap: bool = False)
```

Mean Absolute Deviation

Args:
- period (int) : time period, default 20

## calc_max function

```python
calc_max(series, period, *, wrap: bool = False)
```

Rolling Maximum
## calc_mdi function

```python
calc_mdi(prices, period=14, *, wrap: bool = False)
```

Minus Directional Index

Args:
- period (int) : time period, default 14

## calc_mfi function

```python
calc_mfi(prices, period=14, *, wrap: bool = False)
```

Money Flow Index 

Args:
- period (int) : time period, default 14

## calc_midprice function

```python
calc_midprice(prices, *, wrap: bool = False)
```

Mid Price

Value of (high + low) / 2

## calc_min function

```python
calc_min(series, period, *, wrap: bool = False)
```

Rolling Minimum

Args:
- period (int) : time period, required

## calc_natr function

```python
calc_natr(prices, period=14, *, wrap: bool = False)
```

Average True Range (normalized)

Args:
- period (int) : time period, default 14    

## calc_pdi function

```python
calc_pdi(prices, period=14, *, wrap: bool = False)
```

Plus Directional Index

Args:
- period (int) : time period, default 14

## calc_ppo function

```python
calc_ppo(series, n1=12, n2=26, n3=9, *, wrap: bool = False)
```

Price Percentage Oscillator

Args:
- n1 (int) : short time period, default 12
- n2 (int) : long time period, default 26
- n3 (int) : signal time period, default 9

Outputs:
+ ppo, pposignal, ppohist

## calc_price function

```python
calc_price(prices, item: str = None, *, wrap: bool = False)
```

Generic Price 
   
   Args:
- item (str) : one of 'open', 'high', 'low', 'close',
           'avg', 'mid', 'typ', 'wcl' defaults to 'close'

## calc_rma function

```python
calc_rma(series, period, *, wrap: bool = False)
```

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

## calc_roc function

```python
calc_roc(series, period=1, *, wrap: bool = False)
```

Rate of Change

Args:
- period (int) : time period, default 1

## calc_rsi function

```python
calc_rsi(series, period=14, *, wrap: bool = False)
```

Relative Strength Index

Args:
- period (int) : time period, default 14

## calc_sar function

```python
calc_sar(prices, afs=0.02, maxaf=0.2, *, wrap: bool = False)
```

Parabolic Stop and Reverse

Args:
- afs (float) : starting acceleration factor, default 0.02
- maxaf (float) : maximum acceleration factor, default 0.2

## calc_sign function

```python
calc_sign(series, na_value=nan, wrap: bool = False)
```

Sign
## calc_slope function

```python
calc_slope(series, period=20, *, option=0, offset=0, wrap: bool = False)
```

Slope (time linear regression)

Args:
- period (int) : time period, default 20

## calc_sma function

```python
calc_sma(series, period, *, wrap: bool = False)
```

Simple Moving Average

Args:
- period (int) : time period, required

## calc_stdev function

```python
calc_stdev(series, period=20, *, wrap: bool = False)
```

Standard Deviation

Args:
- period (int) : time period, default 20

## calc_stoch function

```python
calc_stoch(prices, period=14, fastn=3, slown=3, *, wrap: bool = False)
```

Stochastic Oscillator

Args:
- period (int) :  time period of window, default, 14
- fastn (int) : time period of fast average, default 3
- slown (int) : time period of slow average, default 3

## calc_streak function

```python
calc_streak(series, *, wrap: bool = False)
```

Consecutive streak of ups or downs

Length of streak of values all up or down, times +1 or -1 whether ups or downs.

## calc_sum function

```python
calc_sum(series, period, *, wrap: bool = False)
```

Rolling Sum

Args:
- period (int) : time period, required

## calc_tema function

```python
calc_tema(series, period=20, *, wrap: bool = False)
```

Triple Exponential Moving Average

Args:
- period (int) : time period, default 20

## calc_trange function

```python
calc_trange(prices, *, log_prices: bool = False, percent: bool = False, wrap: bool = False)
```

True Range

Args:
- log_percent (bool) : whether to apply log to prices before calculatio
- percent (bool) : result as percentage of price

## calc_typprice function

```python
calc_typprice(prices, *, wrap: bool = False)
```

Typical Price

Value of (high + low + close ) / 3

## calc_updown function

```python
calc_updown(series, up_level=0.0, down_level=0.0, *, wrap: bool = False)
```

Flag for value crossing up & down levels

Args:
- up_level (float) : flag set at 1 above that level
- down_level (float) : flag set at 0 below that level

## calc_wclprice function

```python
calc_wclprice(prices, *, wrap: bool = False)
```

Weighted Close Price

Value of (high + low + 2 * close) / 3

## calc_wma function

```python
calc_wma(series, period, *, wrap: bool = False)
```

Weighted Moving Average
    
Args:
- period (int) : time period, required

## check_size function

```python
check_size(xs, *others)
```

check all series have the same size and return the size
## column_accessor function

```python
column_accessor(data)
```

column accessor if applicable
## crossover function

```python
crossover(series, level=0.0, *, wrap: bool = False)
```

Cross Over

Yields a value of 1 at the point where series crosses over level

Args:
- level (float) : level to cross, default 0.0

## crossunder function

```python
crossunder(series, level=0.0, *, wrap: bool = False)
```

Cross Under

Yields a value of 1 at the point where series crosses under level

Args:
- level (float) : level to cross, default 0.0

## dataframe_like function

```python
dataframe_like(data)
```

check if data is dataframe like
## get_array function

```python
get_array(data, item: str = None, *, default_item: str = 'close', dtype=None)
```

get array from prices or series data
## get_arrays function

```python
get_arrays(data, items: str = None, *, dtype=None)
```

get arrays from prices data
## get_series function

```python
get_series(data, item: str = None, *, default_item: str = 'close')
```

get series from prices or series data
## get_series_old function

```python
get_series_old(data, item: str = None, *, default_item: str = 'close')
```

get series from either series/prices data
## where_flag function

```python
where_flag(flag, x, y, z=nan, *, wrap: bool = False)
```

Value according to flag
## wrap_function function

```python
wrap_function(source, same_scale: bool = None)
```

update function with documentation from source
## wrap_indicator function

```python
wrap_indicator(source)
```

update indicator with documentation from source
## wrap_result function

```python
wrap_result(result, source)
```

wrap result to match source data form (pandas, polars)
