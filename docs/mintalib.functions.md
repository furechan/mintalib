# `mintalib.functions` module

Calculation functions for technical analysis indicators.

The function names are all lower case and may conflict with standard functions,
so the best way to use this module is to alias it to a short name
like `ta` and access all functions as attributes.

The first parameter `series` or `prices` indicates whether the function
accepts a single series or a prices dataframe.

Functions that accept a series usually have an optional parameter `item`
to specify which column to use if the input is a dataframe.

All functions wrap their output to match the type of their input.

In particular the result of a function applied to a pandas series or dataframes
will have the same index as the input.


## `avgprice` function

```python
avgprice(prices)
```

Average Price

Value of (open + high + low + close) / 4

## `typprice` function

```python
typprice(prices)
```

Typical Price

Value of (high + low + close ) / 3

## `wclprice` function

```python
wclprice(prices)
```

Weighted Close Price

Value of (high + low + 2 * close) / 3

## `midprice` function

```python
midprice(prices)
```

Mid Price

Value of (high + low) / 2

## `price` function

```python
price(prices, item: str = None)
```

Generic Price 
   
   Args:
- item (str) : one of 'open', 'high', 'low', 'close',
           'avg', 'mid', 'typ', 'wcl' defaults to 'close'

## `crossover` function

```python
crossover(series, level: float = 0.0, *, item: str = None)
```

Cross Over

Yields a value of 1 at the point where series crosses over level

Args:
- level (float) : level to cross, default 0.0

## `crossunder` function

```python
crossunder(series, level: float = 0.0, *, item: str = None)
```

Cross Under

Yields a value of 1 at the point where series crosses under level

Args:
- level (float) : level to cross, default 0.0

## `flag` function

```python
flag(series, *, item: str = None)
```

Flag for value above zero

## `updown` function

```python
updown(series, up_level: float = 0.0, down_level: float = 0.0, *, item: str = None)
```

Flag for value crossing up & down levels

Args:
- up_level (float) : flag set at 1 above that level
- down_level (float) : flag set at 0 below that level

## `sign` function

```python
sign(series, na_value: float = nan, *, item: str = None)
```

Sign
## `step` function

```python
step(series, threshold: float = 1.0, *, item: str = None)
```

Step Function

Limit value changes to threshold (in absolute value)

Args:
- threshold (float) : threshold value, default 1.0

## `clag` function

```python
clag(series, period: int = 1, *, item: str = None)
```

Confirmation Lag

Changes value only after a confirmation period 

Args:
- period (int) : time period, default 1

## `abs` function

```python
abs(series, *, item: str = None)
```

Absolute Value
## `log` function

```python
log(series, *, item: str = None)
```

Logarithm
## `exp` function

```python
exp(series, *, item: str = None)
```

Exponential
## `diff` function

```python
diff(series, period: int = 1, *, item: str = None)
```

Difference

Difference between current value and the one offset by period

Args:
- period (int) : time period, default 1

## `lag` function

```python
lag(series, period: int, *, item: str = None)
```

Lag Function

Args:
- period (int) : time period, required

## `min` function

```python
min(series, period: int, *, item: str = None)
```

Rolling Minimum

Args:
- period (int) : time period, required

## `max` function

```python
max(series, period: int, *, item: str = None)
```

Rolling Maximum
## `sum` function

```python
sum(series, period: int, *, item: str = None)
```

Rolling Sum

Args:
- period (int) : time period, required

## `roc` function

```python
roc(series, period: int = 1, *, item: str = None)
```

Rate of Change

Args:
- period (int) : time period, default 1

## `mad` function

```python
mad(series, period: int = 20, *, item: str = None)
```

Mean Absolute Deviation

Args:
- period (int) : time period, default 20

## `stdev` function

```python
stdev(series, period: int = 20, *, item: str = None)
```

Standard Deviation

Args:
- period (int) : time period, default 20

## `sma` function

```python
sma(series, period: int, *, item: str = None)
```

Simple Moving Average

Args:
- period (int) : time period, required

## `ema` function

```python
ema(series, period: int, *, adjust: bool = False, item: str = None)
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

## `rma` function

```python
rma(series, period: int, *, item: str = None)
```

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

## `wma` function

```python
wma(series, period: int, *, item: str = None)
```

Weighted Moving Average
    
Args:
- period (int) : time period, required

## `hma` function

```python
hma(series, period: int, *, item: str = None)
```

Hull Moving Average

Args:
- period (int) : time period, required    

## `dema` function

```python
dema(series, period: int, *, item: str = None)
```

Double Exponential Moving Average
 
Args:
- period (int) : time period, required    

## `tema` function

```python
tema(series, period: int = 20, *, item: str = None)
```

Triple Exponential Moving Average

Args:
- period (int) : time period, default 20

## `mav` function

```python
mav(series, period: int = 20, *, ma_type: str = 'SMA', item: str = None)
```

Generic Moving Average

Moving average computed according to ma_type

Args:
- ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
            defaults to 'SMA'

## `rsi` function

```python
rsi(series, period: int = 14, *, item: str = None)
```

Relative Strength Index

Args:
- period (int) : time period, default 14

## `dmi` function

```python
dmi(prices, period: int = 14)
```

Directional Movement Indicator

Args:
- period (int) : time period, default 14

## `adx` function

```python
adx(prices, period: int = 14)
```

Average Directional Index

Args:
- period (int) : time period, default 14

## `pdi` function

```python
pdi(prices, period: int = 14)
```

Plus Directional Index

Args:
- period (int) : time period, default 14

## `mdi` function

```python
mdi(prices, period: int = 14)
```

Minus Directional Index

Args:
- period (int) : time period, default 14

## `trange` function

```python
trange(prices, *, log_prices: bool = False, percent: bool = False)
```

True Range

Args:
- log_percent (bool) : whether to apply log to prices before calculatio
- percent (bool) : result as percentage of price

## `atr` function

```python
atr(prices, period: int = 14)
```

Average True Range

Args:
- period (int) : time period, default 14    

## `natr` function

```python
natr(prices, period: int = 14)
```

Average True Range (normalized)

Args:
- period (int) : time period, default 14    

## `sar` function

```python
sar(prices, afs: float = 0.02, maxaf: float = 0.2)
```

Parabolic Stop and Reverse

Args:
- afs (float) : starting acceleration factor, default 0.02
- maxaf (float) : maximum acceleration factor, default 0.2

## `cci` function

```python
cci(prices, period: int = 20)
```

Commodity Channel Index

Args:
- period (int) : time period, default 20

## `cmf` function

```python
cmf(prices, period: int = 20)
```

Chaikin Money Flow

Args:
- period (int) : time period, default 20

## `mfi` function

```python
mfi(prices, period: int = 14)
```

Money Flow Index 

Args:
- period (int) : time period, default 14

## `bop` function

```python
bop(prices, period: int = 20)
```

Balance of Power

Args:
- period (int) : time period, default 20

## `bbands` function

```python
bbands(prices, period: int = 20, nbdev: float = 2.0)
```

Bollinger Bands

Args:
- period (int) : time period, default 20
- nbdev (float) : bands width in number of standard deviations

## `keltner` function

```python
keltner(prices, period: int = 20, nbatr: float = 2.0)
```

Keltner Channel

Args:
- period (int) : time period, default 20
- nbatr (float) : channel width in number of atrs, default 2.0

## `ker` function

```python
ker(series, period: int = 10, *, item: str = None)
```

Kaufman Efficiency Ratio

Args:
- period (int) : time period, default 10

## `kama` function

```python
kama(series, period: int = 10, fastn: int = 2, slown: int = 30, *, item: str = None)
```

Kaufman Adaptive Moving Average

Args:
- period (int) : time period for efficiency ratio, default 10
- fastn (int) : time period for fast moving average, default, 2
- slown (int) : time period for slow moving average, default 30

## `macd` function

```python
macd(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None)
```

Moving Average Convergenge Divergence

Args:
- n1 (int) : show time period, default 12
- n2 (int) : long time periodm, default 26
- n3 (int) : signal time period, default 9  

Outputs:
+ macd, macdsignal, macdhist

## `ppo` function

```python
ppo(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None)
```

Price Percentage Oscillator

Args:
- n1 (int) : short time period, default 12
- n2 (int) : long time period, default 26
- n3 (int) : signal time period, default 9

Outputs:
+ ppo, pposignal, ppohist

## `slope` function

```python
slope(series, period: int = 20, *, item: str = None)
```

Slope (linear regression)

Args:
- period (int) : time period, default 20

## `rvalue` function

```python
rvalue(series, period: int = 20, *, item: str = None)
```

R-Value (linear regression)

Args:
- period (int) : time period, default 20

## `tsf` function

```python
tsf(series, period: int = 20, offset: int = 0, *, item: str = None)
```

Time Series Forecast (linear regression)

Args:
- period (int) : time period, default 20

## `curve` function

```python
curve(series, period: int = 20, *, item: str = None)
```

Curve (quadratic regression)
## `stoch` function

```python
stoch(prices, period: int = 14, fastn: int = 3, slown: int = 3)
```

Stochastic Oscillator

Args:
- period (int) :  time period of window, default, 14
- fastn (int) : time period of fast average, default 3
- slown (int) : time period of slow average, default 3

## `streak` function

```python
streak(series, *, item: str = None)
```

Consecutive streak of ups or downs

Length of streak of values all up or down, times +1 or -1 whether ups or downs.

## `eval` function

```python
eval(prices, expr: str)
```

Expression Eval (pandas only)

Args:
- expr (str) : expression to eval

