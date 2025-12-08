"""
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
"""

# PREAMBLE Do not edit! This file was generated

import inspect

from . import core
from .core import get_series, wrap_result, column_accessor

nan = float('nan')

def wrap_function(calc_func):

    sig = inspect.signature(calc_func)
    first_param = next(iter(sig.parameters))

    def decorator(func):
        sig = inspect.signature(func)

        def wrapper(prices, *args, **kwargs):
            item = kwargs.pop('item', None)

            if first_param == 'series':
                input = get_series(prices, item)
            else:
                input = column_accessor(prices)

            result = calc_func(input, *args, **kwargs)
            return wrap_result(result, prices)

        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__doc__ = calc_func.__doc__
        wrapper.__signature__ = sig

        return wrapper
    return decorator


@wrap_function(core.calc_abs)
def abs(prices, *, item: str = None): ...

@wrap_function(core.calc_adx)
def adx(prices, period: int = 14): ...

@wrap_function(core.calc_alma)
def alma(prices, period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, item: str = None): ...

@wrap_function(core.calc_atr)
def atr(prices, period: int = 14): ...

@wrap_function(core.calc_avgprice)
def avgprice(prices): ...

@wrap_function(core.calc_bbands)
def bbands(prices, period: int = 20, nbdev: float = 2.0): ...

@wrap_function(core.calc_bbp)
def bbp(prices, period: int = 20, nbdev: float = 2.0): ...

@wrap_function(core.calc_bbw)
def bbw(prices, period: int = 20, nbdev: float = 2.0): ...

@wrap_function(core.calc_bop)
def bop(prices, period: int = 20): ...

@wrap_function(core.calc_cci)
def cci(prices, period: int = 20): ...

@wrap_function(core.calc_clag)
def clag(prices, period: int = 1, *, item: str = None): ...

@wrap_function(core.calc_cmf)
def cmf(prices, period: int = 20): ...

@wrap_function(core.calc_crossover)
def crossover(prices, level: float = 0.0, *, item: str = None): ...

@wrap_function(core.calc_crossunder)
def crossunder(prices, level: float = 0.0, *, item: str = None): ...

@wrap_function(core.calc_curve)
def curve(prices, period: int = 20, *, item: str = None): ...

@wrap_function(core.calc_dema)
def dema(prices, period: int, *, item: str = None): ...

@wrap_function(core.calc_diff)
def diff(prices, period: int = 1, *, item: str = None): ...

@wrap_function(core.calc_dmi)
def dmi(prices, period: int = 14): ...

@wrap_function(core.calc_ema)
def ema(prices, period: int, *, adjust: bool = False, item: str = None): ...

@wrap_function(core.calc_eval)
def eval(prices, expr: str, *, as_flag: bool = False): ...

@wrap_function(core.calc_exp)
def exp(prices, *, item: str = None): ...

@wrap_function(core.calc_flag)
def flag(prices, *, item: str = None): ...

@wrap_function(core.calc_hma)
def hma(prices, period: int, *, item: str = None): ...

@wrap_function(core.calc_kama)
def kama(prices, period: int = 10, fastn: int = 2, slown: int = 30, *, item: str = None): ...

@wrap_function(core.calc_keltner)
def keltner(prices, period: int = 20, nbatr: float = 2.0): ...

@wrap_function(core.calc_ker)
def ker(prices, period: int = 10, *, item: str = None): ...

@wrap_function(core.calc_lag)
def lag(prices, period: int, *, item: str = None): ...

@wrap_function(core.calc_log)
def log(prices, *, item: str = None): ...

@wrap_function(core.calc_lroc)
def lroc(prices, period: int = 1, *, item: str = None): ...

@wrap_function(core.calc_macd)
def macd(prices, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None): ...

@wrap_function(core.calc_macdv)
def macdv(prices, n1: int = 12, n2: int = 26, n3: int = 9): ...

@wrap_function(core.calc_mad)
def mad(prices, period: int = 14, *, item: str = None): ...

@wrap_function(core.calc_mav)
def mav(prices, period: int = 20, *, ma_type: str = 'SMA', item: str = None): ...

@wrap_function(core.calc_max)
def max(prices, period: int, *, item: str = None): ...

@wrap_function(core.calc_mdi)
def mdi(prices, period: int = 14): ...

@wrap_function(core.calc_mfi)
def mfi(prices, period: int = 14): ...

@wrap_function(core.calc_midprice)
def midprice(prices): ...

@wrap_function(core.calc_min)
def min(prices, period: int, *, item: str = None): ...

@wrap_function(core.calc_natr)
def natr(prices, period: int = 14): ...

@wrap_function(core.calc_pdi)
def pdi(prices, period: int = 14): ...

@wrap_function(core.calc_ppo)
def ppo(prices, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None): ...

@wrap_function(core.calc_price)
def price(prices, item: str = None): ...

@wrap_function(core.calc_qsf)
def qsf(prices, period: int = 20, offset: int = 0, *, item: str = None): ...

@wrap_function(core.calc_rma)
def rma(prices, period: int, *, item: str = None): ...

@wrap_function(core.calc_roc)
def roc(prices, period: int = 1, *, item: str = None): ...

@wrap_function(core.calc_rsi)
def rsi(prices, period: int = 14, *, item: str = None): ...

@wrap_function(core.calc_rvalue)
def rvalue(prices, period: int = 20, *, item: str = None): ...

@wrap_function(core.calc_sar)
def sar(prices, afs: float = 0.02, maxaf: float = 0.2): ...

@wrap_function(core.calc_shift)
def shift(prices, period: int, *, item: str = None): ...

@wrap_function(core.calc_sign)
def sign(prices, na_value: float = nan, *, item: str = None): ...

@wrap_function(core.calc_slope)
def slope(prices, period: int = 20, *, item: str = None): ...

@wrap_function(core.calc_sma)
def sma(prices, period: int, *, item: str = None): ...

@wrap_function(core.calc_stdev)
def stdev(prices, period: int = 20, *, item: str = None): ...

@wrap_function(core.calc_step)
def step(prices, threshold: 'float' = 1.0, *, item: str = None): ...

@wrap_function(core.calc_stoch)
def stoch(prices, period: int = 14, fastn: int = 3, slown: int = 3): ...

@wrap_function(core.calc_streak)
def streak(prices, *, item: str = None): ...

@wrap_function(core.calc_sum)
def sum(prices, period: int, *, item: str = None): ...

@wrap_function(core.calc_tema)
def tema(prices, period: int = 20, *, item: str = None): ...

@wrap_function(core.calc_trange)
def trange(prices, *, log_prices: bool = False, percent: bool = False): ...

@wrap_function(core.calc_tsf)
def tsf(prices, period: int = 20, offset: int = 0, *, item: str = None): ...

@wrap_function(core.calc_typprice)
def typprice(prices): ...

@wrap_function(core.calc_updown)
def updown(prices, up_level: float = 0.0, down_level: float = 0.0, *, item: str = None): ...

@wrap_function(core.calc_wclprice)
def wclprice(prices): ...

@wrap_function(core.calc_wma)
def wma(prices, period: int, *, item: str = None): ...

__all__ = [
    'abs', 'adx', 'alma', 'atr', 'avgprice', 'bbands', 'bbp', 'bbw', 'bop',
    'cci', 'clag', 'cmf', 'crossover', 'crossunder', 'curve', 'dema',
    'diff', 'dmi', 'ema', 'eval', 'exp', 'flag', 'hma', 'kama', 'keltner',
    'ker', 'lag', 'log', 'lroc', 'macd', 'macdv', 'mad', 'mav', 'max',
    'mdi', 'mfi', 'midprice', 'min', 'natr', 'pdi', 'ppo', 'price', 'qsf',
    'rma', 'roc', 'rsi', 'rvalue', 'sar', 'shift', 'sign', 'slope', 'sma',
    'stdev', 'step', 'stoch', 'streak', 'sum', 'tema', 'trange', 'tsf',
    'typprice', 'updown', 'wclprice', 'wma'
]
