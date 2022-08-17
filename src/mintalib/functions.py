# Do not edit! File generated automatically...

from . import core
from . import utils


def get_series(data, item=None, *, default_item='close'):
    if hasattr(data, 'columns'):
        if item is None:
            item = default_item

        return data[item]

    if item is not None:
        raise ValueError("Cannot specify item with %s input!", type(data).__name__)

    return data


@utils.wrap_function(core.calc_avgprice)
def avgprice(prices):
    return core.calc_avgprice(prices)


@utils.wrap_function(core.calc_typprice)
def typprice(prices):
    return core.calc_typprice(prices)


@utils.wrap_function(core.calc_wclprice)
def wclprice(prices):
    return core.calc_wclprice(prices)


@utils.wrap_function(core.calc_midprice)
def midprice(prices):
    return core.calc_midprice(prices)


@utils.wrap_function(core.calc_roc)
def roc(series, period: int = 1, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_roc(series, period)


@utils.wrap_function(core.calc_diff)
def diff(series, period: int = 1, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_diff(series, period, wrap=True)


@utils.wrap_function(core.calc_min)
def min(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_min(series, period)


@utils.wrap_function(core.calc_max)
def max(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_max(series, period)


@utils.wrap_function(core.calc_sum)
def sum(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_sum(series, period)


@utils.wrap_function(core.calc_sma)
def sma(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_sma(series, period, wrap=True)


@utils.wrap_function(core.calc_ema)
def ema(series, period: int, *, mixed: bool = True, item: str = None):
    series = get_series(series, item=item)
    return core.calc_ema(series, period, mixed=mixed, wrap=True)


@utils.wrap_function(core.calc_rma)
def rma(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_rma(series, period, wrap=True)


@utils.wrap_function(core.calc_wma)
def wma(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_wma(series, period, wrap=True)


@utils.wrap_function(core.calc_dema)
def dema(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_dema(series, period, wrap=True)


@utils.wrap_function(core.calc_tema)
def tema(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_tema(series, period, wrap=True)


@utils.wrap_function(core.calc_ma)
def ma(series, period: int, *, ma_type: int = 0, item: str = None):
    series = get_series(series, item=item)
    return core.calc_ma(series, period, ma_type=ma_type, wrap=True)


@utils.wrap_function(core.calc_rsi)
def rsi(series, period: int = 14, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_rsi(series, period)


@utils.wrap_function(core.calc_plusdi)
def plusdi(prices, period: int = 14):
    return core.calc_plusdi(prices, period)


@utils.wrap_function(core.calc_minusdi)
def minusdi(prices, period: int = 14):
    return core.calc_minusdi(prices, period)


@utils.wrap_function(core.calc_adx)
def adx(prices, period: int = 14):
    return core.calc_adx(prices, period)


@utils.wrap_function(core.calc_trange)
def trange(prices, *, log_prices: bool = False, percent: bool = False):
    return core.calc_trange(prices, log_prices=log_prices, percent=percent, wrap=True)


@utils.wrap_function(core.calc_atr)
def atr(prices, period: int = 14):
    return core.calc_atr(prices, period)


@utils.wrap_function(core.calc_natr)
def natr(prices, period: int = 14):
    return core.calc_natr(prices, period)


@utils.wrap_function(core.calc_latr)
def latr(prices, period: int = 14):
    return core.calc_latr(prices, period)


@utils.wrap_function(core.calc_psar)
def psar(prices, afs: float = 0.02, maxaf: float = 0.2):
    return core.calc_psar(prices, afs=afs, maxaf=maxaf)


@utils.wrap_function(core.calc_bbands)
def bbands(prices, period: int = 20, nbdev: float = 2.0):
    return core.calc_bbands(prices, period, nbdev=nbdev)


@utils.wrap_function(core.calc_keltner)
def keltner(prices, period: int = 20, nbatr: float = 2.0):
    return core.calc_keltner(prices, period, nbatr=nbatr)


@utils.wrap_function(core.calc_macd)
def macd(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_macd(series, n1=n1, n2=n2, n3=n3)


@utils.wrap_function(core.calc_ppo)
def ppo(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_ppo(series, n1=n1, n2=n2, n3=n3)


@utils.wrap_function(core.calc_slope)
def slope(series, period: int = 20, option: int = 0, offset: int = 0, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_slope(series, period, option=option, offset=offset)


@utils.wrap_function(core.calc_curve)
def curve(series, period: int = 20, option: int = 0, offset: int = 0, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_curve(series, period, option=option, offset=offset)


@utils.wrap_function(core.calc_stdev)
def stdev(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_stdev(series, period)


@utils.wrap_function(core.calc_stoch)
def stoch(prices, period: int = 14, fastn: int = 3, slown: int = 3):
    return core.calc_stoch(prices, period, fastn=fastn, slown=slown, wrap=True)


@utils.wrap_function(core.calc_streak)
def streak(series, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_streak(series)


