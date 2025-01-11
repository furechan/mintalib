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

# Do not edit! This file was generated

from . import core
from .core import get_series, wrap_function, wrap_result


nan = float('nan')

def __getattr__(name):
    if name.isupper() and name.lower() in globals():
        return globals()[name.lower()]
    raise AttributeError(f"Module {__name__} has no attribute {name!r}")

__all__ = ()


@wrap_function(core.calc_avgprice)
def avgprice(prices):
    kwargs = dict()
    result = core.calc_avgprice(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_typprice)
def typprice(prices):
    kwargs = dict()
    result = core.calc_typprice(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_wclprice)
def wclprice(prices):
    kwargs = dict()
    result = core.calc_wclprice(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_midprice)
def midprice(prices):
    kwargs = dict()
    result = core.calc_midprice(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_price)
def price(prices, item: str = None):
    kwargs = dict()
    result = core.calc_price(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_crossover)
def crossover(series, level: float = 0.0, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(level=level)
    result = core.calc_crossover(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_crossunder)
def crossunder(series, level: float = 0.0, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(level=level)
    result = core.calc_crossunder(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_flag)
def flag(series, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict()
    result = core.calc_flag(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_updown)
def updown(series, up_level: float = 0.0, down_level: float = 0.0, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(up_level=up_level, down_level=down_level)
    result = core.calc_updown(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_sign)
def sign(series, na_value: float = nan, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(na_value=na_value)
    result = core.calc_sign(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_step)
def step(series, threshold: 'float' = 1.0, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(threshold=threshold)
    result = core.calc_step(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_clag)
def clag(series, period: int = 1, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_clag(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_abs)
def abs(series, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict()
    result = core.calc_abs(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_log)
def log(series, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict()
    result = core.calc_log(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_exp)
def exp(series, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict()
    result = core.calc_exp(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_diff)
def diff(series, period: int = 1, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_diff(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_lag)
def lag(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_lag(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_min)
def min(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_min(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_max)
def max(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_max(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_sum)
def sum(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_sum(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_roc)
def roc(series, period: int = 1, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_roc(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_lroc)
def lroc(series, period: int = 1, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_lroc(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_mad)
def mad(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_mad(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_stdev)
def stdev(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_stdev(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_mav)
def mav(series, period: int = 20, *, ma_type: str = 'SMA', item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period, ma_type=ma_type)
    result = core.calc_mav(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_sma)
def sma(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_sma(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_ema)
def ema(series, period: int, *, adjust: bool = False, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period, adjust=adjust)
    result = core.calc_ema(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_rma)
def rma(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_rma(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_wma)
def wma(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_wma(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_hma)
def hma(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_hma(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_dema)
def dema(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_dema(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_tema)
def tema(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_tema(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_alma)
def alma(series, period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period, offset=offset, sigma=sigma)
    result = core.calc_alma(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_rsi)
def rsi(series, period: int = 14, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_rsi(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_dmi)
def dmi(prices, period: int = 14):
    kwargs = dict(period=period)
    result = core.calc_dmi(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_adx)
def adx(prices, period: int = 14):
    kwargs = dict(period=period)
    result = core.calc_adx(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_pdi)
def pdi(prices, period: int = 14):
    kwargs = dict(period=period)
    result = core.calc_pdi(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_mdi)
def mdi(prices, period: int = 14):
    kwargs = dict(period=period)
    result = core.calc_mdi(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_trange)
def trange(prices, *, log_prices: bool = False, percent: bool = False):
    kwargs = dict(log_prices=log_prices, percent=percent)
    result = core.calc_trange(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_atr)
def atr(prices, period: int = 14):
    kwargs = dict(period=period)
    result = core.calc_atr(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_natr)
def natr(prices, period: int = 14):
    kwargs = dict(period=period)
    result = core.calc_natr(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_sar)
def sar(prices, afs: float = 0.02, maxaf: float = 0.2):
    kwargs = dict(afs=afs, maxaf=maxaf)
    result = core.calc_sar(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_cci)
def cci(prices, period: int = 20):
    kwargs = dict(period=period)
    result = core.calc_cci(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_cmf)
def cmf(prices, period: int = 20):
    kwargs = dict(period=period)
    result = core.calc_cmf(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_mfi)
def mfi(prices, period: int = 14):
    kwargs = dict(period=period)
    result = core.calc_mfi(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_bop)
def bop(prices, period: int = 20):
    kwargs = dict(period=period)
    result = core.calc_bop(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_bbands)
def bbands(prices, period: int = 20, nbdev: float = 2.0):
    kwargs = dict(period=period, nbdev=nbdev)
    result = core.calc_bbands(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_keltner)
def keltner(prices, period: int = 20, nbatr: float = 2.0):
    kwargs = dict(period=period, nbatr=nbatr)
    result = core.calc_keltner(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_ker)
def ker(series, period: int = 10, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_ker(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_kama)
def kama(series, period: int = 10, fastn: int = 2, slown: int = 30, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period, fastn=fastn, slown=slown)
    result = core.calc_kama(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_macd)
def macd(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(n1=n1, n2=n2, n3=n3)
    result = core.calc_macd(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_ppo)
def ppo(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(n1=n1, n2=n2, n3=n3)
    result = core.calc_ppo(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_slope)
def slope(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_slope(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_rvalue)
def rvalue(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_rvalue(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_tsf)
def tsf(series, period: int = 20, offset: int = 0, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period, offset=offset)
    result = core.calc_tsf(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_curve)
def curve(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict(period=period)
    result = core.calc_curve(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_stoch)
def stoch(prices, period: int = 14, fastn: int = 3, slown: int = 3):
    kwargs = dict(period=period, fastn=fastn, slown=slown)
    result = core.calc_stoch(prices, **kwargs)
    return wrap_result(result, prices)


@wrap_function(core.calc_streak)
def streak(series, *, item: str = None):
    series = get_series(series, item=item)
    kwargs = dict()
    result = core.calc_streak(series, **kwargs)
    return wrap_result(result, series)


@wrap_function(core.calc_eval)
def eval(prices, expr: str, *, as_flag: bool = False):
    kwargs = dict(expr=expr, as_flag=as_flag)
    result = core.calc_eval(prices, **kwargs)
    return wrap_result(result, prices)


