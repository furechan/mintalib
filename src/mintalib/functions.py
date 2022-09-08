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


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_avgprice)
def AVGPRICE(prices):
    return core.calc_avgprice(prices)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_typprice)
def TYPPRICE(prices):
    return core.calc_typprice(prices)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_wclprice)
def WCLPRICE(prices):
    return core.calc_wclprice(prices)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_midprice)
def MIDPRICE(prices):
    return core.calc_midprice(prices)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_log)
def LOG(series, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_log(series)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_exp)
def EXP(series, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_exp(series)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_roc)
def ROC(series, period: int = 1, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_roc(series, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_diff)
def DIFF(series, period: int = 1, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_diff(series, period, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_min)
def MIN(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_min(series, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_max)
def MAX(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_max(series, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_sum)
def SUM(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_sum(series, period, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_mad)
def MAD(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_mad(series, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_stdev)
def STDEV(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_stdev(series, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_sma)
def SMA(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_sma(series, period, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_ema)
def EMA(series, period: int, *, adjust: bool = False, item: str = None):
    series = get_series(series, item=item)
    return core.calc_ema(series, period, adjust=adjust, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_wma)
def WMA(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_wma(series, period, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_dema)
def DEMA(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_dema(series, period, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_tema)
def TEMA(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_tema(series, period, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_ma)
def MA(series, period: int, *, ma_type: int = 0, item: str = None):
    series = get_series(series, item=item)
    return core.calc_ma(series, period, ma_type=ma_type, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_rsi)
def RSI(series, period: int = 14, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_rsi(series, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_plusdi)
def PLUSDI(prices, period: int = 14):
    return core.calc_plusdi(prices, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_minusdi)
def MINUSDI(prices, period: int = 14):
    return core.calc_minusdi(prices, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_adx)
def ADX(prices, period: int = 14):
    return core.calc_adx(prices, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_trange)
def TRANGE(prices, *, log_prices: bool = False, percent: bool = False):
    return core.calc_trange(prices, log_prices=log_prices, percent=percent, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_atr)
def ATR(prices, period: int = 14):
    return core.calc_atr(prices, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_natr)
def NATR(prices, period: int = 14):
    return core.calc_natr(prices, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_latr)
def LATR(prices, period: int = 14):
    return core.calc_latr(prices, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_psar)
def PSAR(prices, afs: float = 0.02, maxaf: float = 0.2):
    return core.calc_psar(prices, afs=afs, maxaf=maxaf)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_cci)
def CCI(prices, period: int = 20):
    return core.calc_cci(prices, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_cmf)
def CMF(prices, period: int = 20):
    return core.calc_cmf(prices, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_mfi)
def MFI(prices, period: int = 14):
    return core.calc_mfi(prices, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_bop)
def BOP(prices, period: int = 20):
    return core.calc_bop(prices, period)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_bbands)
def BBANDS(prices, period: int = 20, nbdev: float = 2.0):
    return core.calc_bbands(prices, period, nbdev=nbdev)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_keltner)
def KELTNER(prices, period: int = 20, nbatr: float = 2.0):
    return core.calc_keltner(prices, period, nbatr=nbatr)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_kama)
def KAMA(series, period: int = 10, fastn: int = 2, slown: int = 30, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_kama(series, period, fastn=fastn, slown=slown, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_macd)
def MACD(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_macd(series, n1=n1, n2=n2, n3=n3, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_ppo)
def PPO(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_ppo(series, n1=n1, n2=n2, n3=n3, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_slope)
def SLOPE(series, period: int = 20, *, option: int = 0, offset: int = 0, item: str = None):
    series = get_series(series, item=item)
    return core.calc_slope(series, period, option=option, offset=offset)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_curve)
def CURVE(series, period: int = 20, *, option: int = 0, offset: int = 0, item: str = None):
    series = get_series(series, item=item)
    return core.calc_curve(series, period, option=option, offset=offset)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_stoch)
def STOCH(prices, period: int = 14, fastn: int = 3, slown: int = 3):
    return core.calc_stoch(prices, period, fastn=fastn, slown=slown, wrap=True)


# noinspection PyPep8Naming
@utils.wrap_function(core.calc_streak)
def STREAK(series, *, item: str = None):
    series = get_series(series, item=item)
    return core.calc_streak(series)


__all__ = [n for n in dir() if n.isupper()]
