# mintalib.functions module

Mintalib Functions

Function names are upper case.

Functions that accept a prices dataframe input have a first paramater called `prices`.
Functions that accept a series input have a fist parameter called `series`,
and an optional parameter `item` to specify which column to use on dataframe inputs.

All functions wrap their output to match the type of their input.
In particular the result of a function applied to a pandas series or dataframes
will have the same index as the input.


## ADX function

```python
ADX(prices, period: int = 14)
```

Average Directional Index

Args:
- period (int) : time period, default 14

## ATR function

```python
ATR(prices, period: int = 14)
```

Average True Range

Args:
- period (int) : time period, default 14    

## AVGPRICE function

```python
AVGPRICE(prices)
```

Average Price

Value of (open + high + low + close) / 4

Attributes:
- same_scale = True

## BBANDS function

```python
BBANDS(prices, period: int = 20, nbdev: float = 2.0)
```

Bollinger Bands

Args:
- period (int) : time period, default 20
- nbdev (float) : bands width in number of standard deviations

Attributes:
- same_scale = True

## BOP function

```python
BOP(prices, period: int = 20)
```

Balance of Power

Args:
- period (int) : time period, default 20

## CCI function

```python
CCI(prices, period: int = 20)
```

Commodity Channel Index

Args:
- period (int) : time period, default 20

## CMF function

```python
CMF(prices, period: int = 20)
```

Chaikin Money Flow

Args:
- period (int) : time period, default 20

## CROSSOVER function

```python
CROSSOVER(series, level: float = 0.0, *, item: str = None)
```

Cross Over

Yields a value of 1 at the point where series crosses over level

Args:
- level (float) : level to cross, default 0.0

## CROSSUNDER function

```python
CROSSUNDER(series, level: float = 0.0, *, item: str = None)
```

Cross Under

Yields a value of 1 at the point where series crosses under level

Args:
- level (float) : level to cross, default 0.0

## CURVE function

```python
CURVE(series, period: int = 20, *, item: str = None)
```

Curve (quadratic regression)
## DEMA function

```python
DEMA(series, period: int, *, item: str = None)
```

Double Exponential Moving Average
 
Args:
- period (int) : time period, required

Attributes:
- same_scale = True

## DIFF function

```python
DIFF(series, period: int = 1, *, item: str = None)
```

Difference

Difference between current value and the one offset by period

Args:
- period (int) : time period, default 1

## DMI function

```python
DMI(prices, period: int = 14)
```

Directional Movement Indicator

Args:
- period (int) : time period, default 14

## EMA function

```python
EMA(series, period: int, *, adjust: bool = False, item: str = None)
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

Attributes:
- same_scale = True

## EVAL function

```python
EVAL(prices, expr: str)
```

Expression Eval (pandas only)

Args:
- expr (str) : expression to eval

## EXP function

```python
EXP(series, *, item: str = None)
```

Exponential
## FLAG function

```python
FLAG(series, *, item: str = None)
```

Flag for value above zero

## HMA function

```python
HMA(series, period: int, *, item: str = None)
```

Hull Moving Average

Args:
- period (int) : time period, required

Attributes:
- same_scale = True

## KAMA function

```python
KAMA(series, period: int = 10, fastn: int = 2, slown: int = 30, *, item: str = None)
```

Kaufman Adaptive Moving Average

Args:
- period (int) : time period for efficiency ratio, default 10
- fastn (int) : time period for fast moving average, default, 2
- slown (int) : time period for slow moving average, default 30

Attributes:
- same_scale = True

## KELTNER function

```python
KELTNER(prices, period: int = 20, nbatr: float = 2.0)
```

Keltner Channel

Args:
- period (int) : time period, default 20
- nbatr (float) : channel width in number of atrs, default 2.0

Attributes:
- same_scale = True

## KER function

```python
KER(series, period: int = 10, *, item: str = None)
```

Kaufman Efficiency Ratio

Args:
- period (int) : time period, default 10

## LAG function

```python
LAG(series, period: int, *, item: str = None)
```

Lag Function

Args:
- period (int) : time period, required

## LOG function

```python
LOG(series, *, item: str = None)
```

Logarithm
## MA function

```python
MA(series, period: int = 20, *, ma_type: str = 'SMA', item: str = None)
```

Generic Moving Average

Moving average computed according to ma_type

Args:
- ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
            defaults to 'SMA'

Attributes:
- same_scale = True

## MACD function

```python
MACD(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None)
```

Moving Average Convergenge Divergence

Args:
- n1 (int) : show time period, default 12
- n2 (int) : long time periodm, default 26
- n3 (int) : signal time period, default 9  

Outputs:
+ macd, macdsignal, macdhist

## MAD function

```python
MAD(series, period: int = 20, *, item: str = None)
```

Mean Absolute Deviation

Args:
- period (int) : time period, default 20

## MAX function

```python
MAX(series, period: int, *, item: str = None)
```

Rolling Maximum

+ Attributes:
- same_scale = True

## MDI function

```python
MDI(prices, period: int = 14)
```

Minus Directional Index

Args:
- period (int) : time period, default 14

## MFI function

```python
MFI(prices, period: int = 14)
```

Money Flow Index 

Args:
- period (int) : time period, default 14

## MIDPRICE function

```python
MIDPRICE(prices)
```

Mid Price

Value of (high + low) / 2

Attributes:
- same_scale = True

## MIN function

```python
MIN(series, period: int, *, item: str = None)
```

Rolling Minimum

Args:
- period (int) : time period, required

Attributes:
- same_scale = True

## NATR function

```python
NATR(prices, period: int = 14)
```

Average True Range (normalized)

Args:
- period (int) : time period, default 14    

## PDI function

```python
PDI(prices, period: int = 14)
```

Plus Directional Index

Args:
- period (int) : time period, default 14

## PPO function

```python
PPO(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None)
```

Price Percentage Oscillator

Args:
- n1 (int) : short time period, default 12
- n2 (int) : long time period, default 26
- n3 (int) : signal time period, default 9

Outputs:
+ ppo, pposignal, ppohist

## PRICE function

```python
PRICE(prices, item: str = None)
```

Generic Price 
   
   Args:
- item (str) : one of 'open', 'high', 'low', 'close',
           'avg', 'mid', 'typ', 'wcl' defaults to 'close'

+ Attributes:
- same_scale = True

## RMA function

```python
RMA(series, period: int, *, item: str = None)
```

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

Attributes:
- same_scale = True

## ROC function

```python
ROC(series, period: int = 1, *, item: str = None)
```

Rate of Change

Args:
- period (int) : time period, default 1

## RSI function

```python
RSI(series, period: int = 14, *, item: str = None)
```

Relative Strength Index

Args:
- period (int) : time period, default 14

## RVALUE function

```python
RVALUE(series, period: int = 20, *, item: str = None)
```

R-Value (linear regression)

Args:
- period (int) : time period, default 20

## SAR function

```python
SAR(prices, afs: float = 0.02, maxaf: float = 0.2)
```

Parabolic Stop and Reverse

Args:
- afs (float) : starting acceleration factor, default 0.02
- maxaf (float) : maximum acceleration factor, default 0.2

Attributes:
- same_scale = True

## SIGN function

```python
SIGN(series, item: str = None)
```

Sign
## SLOPE function

```python
SLOPE(series, period: int = 20, *, item: str = None)
```

Slope (linear regression)

Args:
- period (int) : time period, default 20

## SMA function

```python
SMA(series, period: int, *, item: str = None)
```

Simple Moving Average

Args:
- period (int) : time period, required

Attributes:
- same_scale = True

## STDEV function

```python
STDEV(series, period: int = 20, *, item: str = None)
```

Standard Deviation

Args:
- period (int) : time period, default 20

## STOCH function

```python
STOCH(prices, period: int = 14, fastn: int = 3, slown: int = 3)
```

Stochastic Oscillator

Args:
- period (int) :  time period of window, default, 14
- fastn (int) : time period of fast average, default 3
- slown (int) : time period of slow average, default 3

## STREAK function

```python
STREAK(series, *, item: str = None)
```

Consecutive streak of ups or downs

Length of streak of values all up or down, times +1 or -1 whether ups or downs.

## SUM function

```python
SUM(series, period: int, *, item: str = None)
```

Rolling Sum

Args:
- period (int) : time period, required

## TEMA function

```python
TEMA(series, period: int = 20, *, item: str = None)
```

Triple Exponential Moving Average

Args:
- period (int) : time period, default 20

Attributes:
- same_scale = True

## TRANGE function

```python
TRANGE(prices, *, log_prices: bool = False, percent: bool = False)
```

True Range

Args:
- log_percent (bool) : whether to apply log to prices before calculatio
- percent (bool) : result as percentage of price

## TSF function

```python
TSF(series, period: int = 20, offset: int = 0, *, item: str = None)
```

Time Series Forecast (linear regression)

Args:
- period (int) : time period, default 20

## TYPPRICE function

```python
TYPPRICE(prices)
```

Typical Price

Value of (high + low + close ) / 3

Attributes:
- same_scale = True

## UPDOWN function

```python
UPDOWN(series, up_level=0.0, down_level=0.0, *, item: str = None)
```

Flag for value crossing up & down levels

Args:
- up_level (float) : flag set at 1 above that level
- down_level (float) : flag set at 0 below that level

## WCLPRICE function

```python
WCLPRICE(prices)
```

Weighted Close Price

Value of (high + low + 2 * close) / 3

Attributes:
- same_scale = True

## WMA function

```python
WMA(series, period: int, *, item: str = None)
```

Weighted Moving Average
    
Args:
- period (int) : time period, required

Attributes:
- same_scale = True

