# mintalib.indicators module

Mintalib Indicators

Indicators names are upper case.

Indicators offer a composable interface where a function is bound with its calculation parameters.
When instantiated with parameters an indicator yields a callable that can be applied to prices or series data.
Indicators support the `@` operator as syntactic sugar to apply the indicator to data.
So for example `SMA(50) @ prices` can be used to compute the 50 period simple moving average on `prices`,
insted of `SMA(50)(prices)`.


## ADX indicator

```python
ADX(period: int = 14)
```

Average Directional Index

Args:
- period (int) : time period, default 14

## ATR indicator

```python
ATR(period: int = 14)
```

Average True Range

Args:
- period (int) : time period, default 14    

## AVGPRICE indicator

```python
AVGPRICE()
```

Average Price

Value of (open + high + low + close) / 4

Attributes:
- same_scale = True

## BBANDS indicator

```python
BBANDS(period: int = 20, nbdev: float = 2.0)
```

Bollinger Bands

Args:
- period (int) : time period, default 20
- nbdev (float) : bands width in number of standard deviations

Attributes:
- same_scale = True

## BOP indicator

```python
BOP(period: int = 20)
```

Balance of Power

Args:
- period (int) : time period, default 20

## CCI indicator

```python
CCI(period: int = 20)
```

Commodity Channel Index

Args:
- period (int) : time period, default 20

## CMF indicator

```python
CMF(period: int = 20)
```

Chaikin Money Flow

Args:
- period (int) : time period, default 20

## CROSSOVER indicator

```python
CROSSOVER(level: float = 0.0, *, item: str = None)
```

Cross Over

Yields a value of 1 at the point where series crosses over level

Args:
- level (float) : level to cross, default 0.0

## CROSSUNDER indicator

```python
CROSSUNDER(level: float = 0.0, *, item: str = None)
```

Cross Under

Yields a value of 1 at the point where series crosses under level

Args:
- level (float) : level to cross, default 0.0

## CURVE indicator

```python
CURVE(period: int = 20, *, item: str = None)
```

Curve (time curvilinear regression)
## DEMA indicator

```python
DEMA(period: int, *, item: str = None)
```

Double Exponential Moving Average
 
Args:
- period (int) : time period, required

Attributes:
- same_scale = True

## DIFF indicator

```python
DIFF(period: int = 1, *, item: str = None)
```

Difference

Difference between current value and the one offset by period

Args:
- period (int) : time period, default 1

## DMI indicator

```python
DMI(period: int = 14)
```

Directional Movement Indicator

Args:
- period (int) : time period, default 14

## EMA indicator

```python
EMA(period: int, *, adjust: bool = False, item: str = None)
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

## EVAL indicator

```python
EVAL(expr: str)
```

Expression Eval (pandas only)

Args:
- expr (str) : expression to eval

## EXP indicator

```python
EXP(*, item: str = None)
```

Exponential
## FLAG indicator

```python
FLAG(*, item: str = None)
```

Flag for value above zero

## FORECAST indicator

```python
FORECAST(period: int = 20, offset: int = 0, *, item: str = None)
```

Forecast (time linear regression)
## HMA indicator

```python
HMA(period: int, *, item: str = None)
```

Hull Moving Average

Args:
- period (int) : time period, required

Attributes:
- same_scale = True

## KAMA indicator

```python
KAMA(period: int = 10, fastn: int = 2, slown: int = 30, *, item: str = None)
```

Kaufman Adaptive Moving Average

Args:
- period (int) : time period for efficiency ratio, default 10
- fastn (int) : time period for fast moving average, default, 2
- slown (int) : time period for slow moving average, default 30

Attributes:
- same_scale = True

## KELTNER indicator

```python
KELTNER(period: int = 20, nbatr: float = 2.0)
```

Keltner Channel

Args:
- period (int) : time period, default 20
- nbatr (float) : channel width in number of atrs, default 2.0

Attributes:
- same_scale = True

## KER indicator

```python
KER(period: int = 10, *, item: str = None)
```

Kaufman Efficiency Ratio

Args:
- period (int) : time period, default 10

## LAG indicator

```python
LAG(period: int, *, item: str = None)
```

Lag Function

Args:
- period (int) : time period, required

## LOG indicator

```python
LOG(*, item: str = None)
```

Logarithm
## MA indicator

```python
MA(period: int = 20, *, ma_type: str = None, item: str = None)
```

Generic Moving Average

Moving average computed according to ma_type

Args:
- ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
            defaults to 'SMA'

Attributes:
- same_scale = True

## MACD indicator

```python
MACD(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None)
```

Moving Average Convergenge Divergence

Args:
- n1 (int) : show time period, default 12
- n2 (int) : long time periodm, default 26
- n3 (int) : signal time period, default 9  

Outputs:
+ macd, macdsignal, macdhist

## MAD indicator

```python
MAD(period: int = 20, *, item: str = None)
```

Mean Absolute Deviation

Args:
- period (int) : time period, default 20

## MAX indicator

```python
MAX(period: int, *, item: str = None)
```

Rolling Maximum

+ Attributes:
- same_scale = True

## MDI indicator

```python
MDI(period: int = 14)
```

Minus Directional Index

Args:
- period (int) : time period, default 14

## MFI indicator

```python
MFI(period: int = 14)
```

Money Flow Index 

Args:
- period (int) : time period, default 14

## MIDPRICE indicator

```python
MIDPRICE()
```

Mid Price

Value of (high + low) / 2

Attributes:
- same_scale = True

## MIN indicator

```python
MIN(period: int, *, item: str = None)
```

Rolling Minimum

Args:
- period (int) : time period, required

Attributes:
- same_scale = True

## NATR indicator

```python
NATR(period: int = 14)
```

Average True Range (normalized)

Args:
- period (int) : time period, default 14    

## PDI indicator

```python
PDI(period: int = 14)
```

Plus Directional Index

Args:
- period (int) : time period, default 14

## PPO indicator

```python
PPO(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None)
```

Price Percentage Oscillator

Args:
- n1 (int) : short time period, default 12
- n2 (int) : long time period, default 26
- n3 (int) : signal time period, default 9

Outputs:
+ ppo, pposignal, ppohist

## PRICE indicator

```python
PRICE(item: str = None)
```

Generic Price 
   
   Args:
- item (str) : one of 'open', 'high', 'low', 'close',
           'avg', 'mid', 'typ', 'wcl' defaults to 'close'

+ Attributes:
- same_scale = True

## RMA indicator

```python
RMA(period: int, *, item: str = None)
```

Rolling Moving Average (RSI style)

Exponential moving average with `alpha = 2 / period`,
that starts as a simple moving average until
number of bars is equal to `period`.

Attributes:
- same_scale = True

## ROC indicator

```python
ROC(period: int = 1, *, item: str = None)
```

Rate of Change

Args:
- period (int) : time period, default 1

## RSI indicator

```python
RSI(period: int = 14, *, item: str = None)
```

Relative Strength Index

Args:
- period (int) : time period, default 14

## RVALUE indicator

```python
RVALUE(period: int = 20, *, item: str = None)
```

RValue (time linear regression)
## SAR indicator

```python
SAR(afs: float = 0.02, maxaf: float = 0.2)
```

Parabolic Stop and Reverse

Args:
- afs (float) : starting acceleration factor, default 0.02
- maxaf (float) : maximum acceleration factor, default 0.2

Attributes:
- same_scale = True

## SIGN indicator

```python
SIGN(item: str = None)
```

Sign
## SLOPE indicator

```python
SLOPE(period: int = 20, *, item: str = None)
```

Slope (time linear regression)
## SMA indicator

```python
SMA(period: int, *, item: str = None)
```

Simple Moving Average

Args:
- period (int) : time period, required

Attributes:
- same_scale = True

## STDEV indicator

```python
STDEV(period: int = 20, *, item: str = None)
```

Standard Deviation

Args:
- period (int) : time period, default 20

## STOCH indicator

```python
STOCH(period: int = 14, fastn: int = 3, slown: int = 3)
```

Stochastic Oscillator

Args:
- period (int) :  time period of window, default, 14
- fastn (int) : time period of fast average, default 3
- slown (int) : time period of slow average, default 3

## STREAK indicator

```python
STREAK(*, item: str = None)
```

Consecutive streak of ups or downs

Length of streak of values all up or down, times +1 or -1 whether ups or downs.

## SUM indicator

```python
SUM(period: int, *, item: str = None)
```

Rolling Sum

Args:
- period (int) : time period, required

## TEMA indicator

```python
TEMA(period: int = 20, *, item: str = None)
```

Triple Exponential Moving Average

Args:
- period (int) : time period, default 20

Attributes:
- same_scale = True

## TRANGE indicator

```python
TRANGE(*, log_prices: bool = False, percent: bool = False)
```

True Range

Args:
- log_percent (bool) : whether to apply log to prices before calculatio
- percent (bool) : result as percentage of price

## TYPPRICE indicator

```python
TYPPRICE()
```

Typical Price

Value of (high + low + close ) / 3

Attributes:
- same_scale = True

## UPDOWN indicator

```python
UPDOWN(up_level: float = 0.0, down_level: float = 0.0, *, item: str = None)
```

Flag for value crossing up & down levels

Args:
- up_level (float) : flag set at 1 above that level
- down_level (float) : flag set at 0 below that level

## WCLPRICE indicator

```python
WCLPRICE()
```

Weighted Close Price

Value of (high + low + 2 * close) / 3

Attributes:
- same_scale = True

## WMA indicator

```python
WMA(period: int, *, item: str = None)
```

Weighted Moving Average
    
Args:
- period (int) : time period, required

Attributes:
- same_scale = True

