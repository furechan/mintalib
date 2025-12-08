"""
Factory functions for technical analysis indicators.

Indicator factory names are all upper case.

Indicators offer a composable interface where a calculation routine
is bound together with its calculation parameters.

An indicator object is a callable that can be applied to prices or series data.

Indicators can be chained with the `@` operator as in `ROC(1) @ SMA(20)`.

The `@` operator can also be used to apply an indicator to its parameter.

So for example `SMA(50) @ prices` can be used to compute the 50 period simple moving average on `prices`,
instead of the more verbose `SMA(50)(prices)`.
"""

# PREAMBLE Do not edit! This file was generated

import inspect

from . import core
from .model import FuncIndicator

nan = float('nan')

def wrap_indicator(calc_func):
    """Decorator to wrap indicators"""

    def decorator(func):
        name = func.__name__
        sig = inspect.signature(func)

        def wrapper(*args, **kwargs):
            binding = sig.bind(*args, **kwargs)
            binding.apply_defaults()
            params = dict(binding.arguments)

            return FuncIndicator(
                name=name,
                func=calc_func,
                params=params,
            )

        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__doc__ = calc_func.__doc__
        wrapper.__signature__ = sig

        return wrapper

    return decorator


@wrap_indicator(core.calc_abs)
def ABS(*, item: str = None): ...

@wrap_indicator(core.calc_adx)
def ADX(period: int = 14): ...

@wrap_indicator(core.calc_alma)
def ALMA(period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, item: str = None): ...

@wrap_indicator(core.calc_atr)
def ATR(period: int = 14): ...

@wrap_indicator(core.calc_avgprice)
def AVGPRICE(): ...

@wrap_indicator(core.calc_bbands)
def BBANDS(period: int = 20, nbdev: float = 2.0): ...

@wrap_indicator(core.calc_bbp)
def BBP(period: int = 20, nbdev: float = 2.0): ...

@wrap_indicator(core.calc_bbw)
def BBW(period: int = 20, nbdev: float = 2.0): ...

@wrap_indicator(core.calc_bop)
def BOP(period: int = 20): ...

@wrap_indicator(core.calc_cci)
def CCI(period: int = 20): ...

@wrap_indicator(core.calc_clag)
def CLAG(period: int = 1, *, item: str = None): ...

@wrap_indicator(core.calc_cmf)
def CMF(period: int = 20): ...

@wrap_indicator(core.calc_crossover)
def CROSSOVER(level: float = 0.0, *, item: str = None): ...

@wrap_indicator(core.calc_crossunder)
def CROSSUNDER(level: float = 0.0, *, item: str = None): ...

@wrap_indicator(core.calc_curve)
def CURVE(period: int = 20, *, item: str = None): ...

@wrap_indicator(core.calc_dema)
def DEMA(period: int, *, item: str = None): ...

@wrap_indicator(core.calc_diff)
def DIFF(period: int = 1, *, item: str = None): ...

@wrap_indicator(core.calc_dmi)
def DMI(period: int = 14): ...

@wrap_indicator(core.calc_ema)
def EMA(period: int, *, adjust: bool = False, item: str = None): ...

@wrap_indicator(core.calc_eval)
def EVAL(expr: str, *, as_flag: bool = False): ...

@wrap_indicator(core.calc_exp)
def EXP(*, item: str = None): ...

@wrap_indicator(core.calc_flag)
def FLAG(*, item: str = None): ...

@wrap_indicator(core.calc_hma)
def HMA(period: int, *, item: str = None): ...

@wrap_indicator(core.calc_kama)
def KAMA(period: int = 10, fastn: int = 2, slown: int = 30, *, item: str = None): ...

@wrap_indicator(core.calc_keltner)
def KELTNER(period: int = 20, nbatr: float = 2.0): ...

@wrap_indicator(core.calc_ker)
def KER(period: int = 10, *, item: str = None): ...

@wrap_indicator(core.calc_lag)
def LAG(period: int, *, item: str = None): ...

@wrap_indicator(core.calc_log)
def LOG(*, item: str = None): ...

@wrap_indicator(core.calc_lroc)
def LROC(period: int = 1, *, item: str = None): ...

@wrap_indicator(core.calc_macd)
def MACD(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None): ...

@wrap_indicator(core.calc_macdv)
def MACDV(n1: int = 12, n2: int = 26, n3: int = 9): ...

@wrap_indicator(core.calc_mad)
def MAD(period: int = 14, *, item: str = None): ...

@wrap_indicator(core.calc_mav)
def MAV(period: int = 20, *, ma_type: str = 'SMA', item: str = None): ...

@wrap_indicator(core.calc_max)
def MAX(period: int, *, item: str = None): ...

@wrap_indicator(core.calc_mdi)
def MDI(period: int = 14): ...

@wrap_indicator(core.calc_mfi)
def MFI(period: int = 14): ...

@wrap_indicator(core.calc_midprice)
def MIDPRICE(): ...

@wrap_indicator(core.calc_min)
def MIN(period: int, *, item: str = None): ...

@wrap_indicator(core.calc_natr)
def NATR(period: int = 14): ...

@wrap_indicator(core.calc_pdi)
def PDI(period: int = 14): ...

@wrap_indicator(core.calc_ppo)
def PPO(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None): ...

@wrap_indicator(core.calc_price)
def PRICE(item: str = None): ...

@wrap_indicator(core.calc_qsf)
def QSF(period: int = 20, offset: int = 0, *, item: str = None): ...

@wrap_indicator(core.calc_rma)
def RMA(period: int, *, item: str = None): ...

@wrap_indicator(core.calc_roc)
def ROC(period: int = 1, *, item: str = None): ...

@wrap_indicator(core.calc_rsi)
def RSI(period: int = 14, *, item: str = None): ...

@wrap_indicator(core.calc_rvalue)
def RVALUE(period: int = 20, *, item: str = None): ...

@wrap_indicator(core.calc_sar)
def SAR(afs: float = 0.02, maxaf: float = 0.2): ...

@wrap_indicator(core.calc_shift)
def SHIFT(period: int, *, item: str = None): ...

@wrap_indicator(core.calc_sign)
def SIGN(na_value: float = nan, *, item: str = None): ...

@wrap_indicator(core.calc_slope)
def SLOPE(period: int = 20, *, item: str = None): ...

@wrap_indicator(core.calc_sma)
def SMA(period: int, *, item: str = None): ...

@wrap_indicator(core.calc_stdev)
def STDEV(period: int = 20, *, item: str = None): ...

@wrap_indicator(core.calc_step)
def STEP(threshold: 'float' = 1.0, *, item: str = None): ...

@wrap_indicator(core.calc_stoch)
def STOCH(period: int = 14, fastn: int = 3, slown: int = 3): ...

@wrap_indicator(core.calc_streak)
def STREAK(*, item: str = None): ...

@wrap_indicator(core.calc_sum)
def SUM(period: int, *, item: str = None): ...

@wrap_indicator(core.calc_tema)
def TEMA(period: int = 20, *, item: str = None): ...

@wrap_indicator(core.calc_trange)
def TRANGE(*, log_prices: bool = False, percent: bool = False): ...

@wrap_indicator(core.calc_tsf)
def TSF(period: int = 20, offset: int = 0, *, item: str = None): ...

@wrap_indicator(core.calc_typprice)
def TYPPRICE(): ...

@wrap_indicator(core.calc_updown)
def UPDOWN(up_level: float = 0.0, down_level: float = 0.0, *, item: str = None): ...

@wrap_indicator(core.calc_wclprice)
def WCLPRICE(): ...

@wrap_indicator(core.calc_wma)
def WMA(period: int, *, item: str = None): ...

__all__ = [
    'ABS', 'ADX', 'ALMA', 'ATR', 'AVGPRICE', 'BBANDS', 'BBP', 'BBW', 'BOP',
    'CCI', 'CLAG', 'CMF', 'CROSSOVER', 'CROSSUNDER', 'CURVE', 'DEMA',
    'DIFF', 'DMI', 'EMA', 'EVAL', 'EXP', 'FLAG', 'HMA', 'KAMA', 'KELTNER',
    'KER', 'LAG', 'LOG', 'LROC', 'MACD', 'MACDV', 'MAD', 'MAV', 'MAX',
    'MDI', 'MFI', 'MIDPRICE', 'MIN', 'NATR', 'PDI', 'PPO', 'PRICE', 'QSF',
    'RMA', 'ROC', 'RSI', 'RVALUE', 'SAR', 'SHIFT', 'SIGN', 'SLOPE', 'SMA',
    'STDEV', 'STEP', 'STOCH', 'STREAK', 'SUM', 'TEMA', 'TRANGE', 'TSF',
    'TYPPRICE', 'UPDOWN', 'WCLPRICE', 'WMA'
]
