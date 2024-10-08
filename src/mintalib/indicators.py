
""" Mintalib Indicators """

# Do not edit! This file was generated by make-indicators.ipynb

from . import core
from . import model

nan = float('nan')

@core.wrap_function(core.AVGPRICE)
class AVGPRICE(model.Indicator):
    def __call__(self, prices):
        return core.AVGPRICE(prices)


@core.wrap_function(core.TYPPRICE)
class TYPPRICE(model.Indicator):
    def __call__(self, prices):
        return core.TYPPRICE(prices)


@core.wrap_function(core.WCLPRICE)
class WCLPRICE(model.Indicator):
    def __call__(self, prices):
        return core.WCLPRICE(prices)


@core.wrap_function(core.MIDPRICE)
class MIDPRICE(model.Indicator):
    def __call__(self, prices):
        return core.MIDPRICE(prices)


@core.wrap_function(core.PRICE)
class PRICE(model.Indicator):
    def __init__(self, item: str = None):
        self.item = item

    def __call__(self, prices):
        return core.PRICE(prices, item=self.item)


@core.wrap_function(core.CROSSOVER)
class CROSSOVER(model.Indicator):
    def __init__(self, level: float = 0.0, *, item: str = None):
        self.level = level
        self.item = item

    def __call__(self, series):
        return core.CROSSOVER(series, level=self.level, item=self.item)


@core.wrap_function(core.CROSSUNDER)
class CROSSUNDER(model.Indicator):
    def __init__(self, level: float = 0.0, *, item: str = None):
        self.level = level
        self.item = item

    def __call__(self, series):
        return core.CROSSUNDER(series, level=self.level, item=self.item)


@core.wrap_function(core.FLAG_ABOVE)
class FLAG_ABOVE(model.Indicator):
    def __init__(self, level: float = 0.0, *, item: str = None):
        self.level = level
        self.item = item

    def __call__(self, series):
        return core.FLAG_ABOVE(series, level=self.level, item=self.item)


@core.wrap_function(core.FLAG_BELOW)
class FLAG_BELOW(model.Indicator):
    def __init__(self, level: float = 0.0, *, item: str = None):
        self.level = level
        self.item = item

    def __call__(self, series):
        return core.FLAG_BELOW(series, level=self.level, item=self.item)


@core.wrap_function(core.FLAG_INVERT)
class FLAG_INVERT(model.Indicator):
    def __init__(self, *, item: str = None):
        self.item = item

    def __call__(self, series):
        return core.FLAG_INVERT(series, item=self.item)


@core.wrap_function(core.FLAG_UPDOWN)
class FLAG_UPDOWN(model.Indicator):
    def __init__(self, up_level: float = 0.0, down_level: float = 0.0, *, item: str = None):
        self.up_level = up_level
        self.down_level = down_level
        self.item = item

    def __call__(self, series):
        return core.FLAG_UPDOWN(series, up_level=self.up_level, down_level=self.down_level, item=self.item)


@core.wrap_function(core.LOG)
class LOG(model.Indicator):
    def __init__(self, *, item: str = None):
        self.item = item

    def __call__(self, series):
        return core.LOG(series, item=self.item)


@core.wrap_function(core.EXP)
class EXP(model.Indicator):
    def __init__(self, *, item: str = None):
        self.item = item

    def __call__(self, series):
        return core.EXP(series, item=self.item)


@core.wrap_function(core.ROC)
class ROC(model.Indicator):
    def __init__(self, period: int = 1, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.ROC(series, period=self.period, item=self.item)


@core.wrap_function(core.DIFF)
class DIFF(model.Indicator):
    def __init__(self, period: int = 1, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.DIFF(series, period=self.period, item=self.item)


@core.wrap_function(core.MIN)
class MIN(model.Indicator):
    def __init__(self, period: int, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.MIN(series, period=self.period, item=self.item)


@core.wrap_function(core.MAX)
class MAX(model.Indicator):
    def __init__(self, period: int, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.MAX(series, period=self.period, item=self.item)


@core.wrap_function(core.SUM)
class SUM(model.Indicator):
    def __init__(self, period: int, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.SUM(series, period=self.period, item=self.item)


@core.wrap_function(core.MAD)
class MAD(model.Indicator):
    def __init__(self, period: int = 20, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.MAD(series, period=self.period, item=self.item)


@core.wrap_function(core.STDEV)
class STDEV(model.Indicator):
    def __init__(self, period: int = 20, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.STDEV(series, period=self.period, item=self.item)


@core.wrap_function(core.SMA)
class SMA(model.Indicator):
    def __init__(self, period: int, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.SMA(series, period=self.period, item=self.item)


@core.wrap_function(core.EMA)
class EMA(model.Indicator):
    def __init__(self, period: int, *, adjust: bool = False, item: str = None):
        self.period = period
        self.adjust = adjust
        self.item = item

    def __call__(self, series):
        return core.EMA(series, period=self.period, adjust=self.adjust, item=self.item)


@core.wrap_function(core.RMA)
class RMA(model.Indicator):
    def __init__(self, period: int, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.RMA(series, period=self.period, item=self.item)


@core.wrap_function(core.WMA)
class WMA(model.Indicator):
    def __init__(self, period: int, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.WMA(series, period=self.period, item=self.item)


@core.wrap_function(core.HMA)
class HMA(model.Indicator):
    def __init__(self, period: int, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.HMA(series, period=self.period, item=self.item)


@core.wrap_function(core.DEMA)
class DEMA(model.Indicator):
    def __init__(self, period: int, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.DEMA(series, period=self.period, item=self.item)


@core.wrap_function(core.TEMA)
class TEMA(model.Indicator):
    def __init__(self, period: int = 20, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.TEMA(series, period=self.period, item=self.item)


@core.wrap_function(core.MA)
class MA(model.Indicator):
    def __init__(self, period: int = 20, *, ma_type: str = None, item: str = None):
        self.period = period
        self.ma_type = ma_type
        self.item = item

    def __call__(self, series):
        return core.MA(series, period=self.period, ma_type=self.ma_type, item=self.item)


@core.wrap_function(core.RSI)
class RSI(model.Indicator):
    def __init__(self, period: int = 14, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.RSI(series, period=self.period, item=self.item)


@core.wrap_function(core.PLUSDI)
class PLUSDI(model.Indicator):
    def __init__(self, period: int = 14):
        self.period = period

    def __call__(self, prices):
        return core.PLUSDI(prices, period=self.period)


@core.wrap_function(core.MINUSDI)
class MINUSDI(model.Indicator):
    def __init__(self, period: int = 14):
        self.period = period

    def __call__(self, prices):
        return core.MINUSDI(prices, period=self.period)


@core.wrap_function(core.ADX)
class ADX(model.Indicator):
    def __init__(self, period: int = 14):
        self.period = period

    def __call__(self, prices):
        return core.ADX(prices, period=self.period)


@core.wrap_function(core.TRANGE)
class TRANGE(model.Indicator):
    def __init__(self, *, log_prices: bool = False, percent: bool = False):
        self.log_prices = log_prices
        self.percent = percent

    def __call__(self, prices):
        return core.TRANGE(prices, log_prices=self.log_prices, percent=self.percent)


@core.wrap_function(core.ATR)
class ATR(model.Indicator):
    def __init__(self, period: int = 14):
        self.period = period

    def __call__(self, prices):
        return core.ATR(prices, period=self.period)


@core.wrap_function(core.NATR)
class NATR(model.Indicator):
    def __init__(self, period: int = 14):
        self.period = period

    def __call__(self, prices):
        return core.NATR(prices, period=self.period)


@core.wrap_function(core.LATR)
class LATR(model.Indicator):
    def __init__(self, period: int = 14):
        self.period = period

    def __call__(self, prices):
        return core.LATR(prices, period=self.period)


@core.wrap_function(core.SAR)
class SAR(model.Indicator):
    def __init__(self, afs: float = 0.02, maxaf: float = 0.2):
        self.afs = afs
        self.maxaf = maxaf

    def __call__(self, prices):
        return core.SAR(prices, afs=self.afs, maxaf=self.maxaf)


@core.wrap_function(core.CCI)
class CCI(model.Indicator):
    def __init__(self, period: int = 20):
        self.period = period

    def __call__(self, prices):
        return core.CCI(prices, period=self.period)


@core.wrap_function(core.CMF)
class CMF(model.Indicator):
    def __init__(self, period: int = 20):
        self.period = period

    def __call__(self, prices):
        return core.CMF(prices, period=self.period)


@core.wrap_function(core.MFI)
class MFI(model.Indicator):
    def __init__(self, period: int = 14):
        self.period = period

    def __call__(self, prices):
        return core.MFI(prices, period=self.period)


@core.wrap_function(core.BOP)
class BOP(model.Indicator):
    def __init__(self, period: int = 20):
        self.period = period

    def __call__(self, prices):
        return core.BOP(prices, period=self.period)


@core.wrap_function(core.BBANDS)
class BBANDS(model.Indicator):
    def __init__(self, period: int = 20, nbdev: float = 2.0):
        self.period = period
        self.nbdev = nbdev

    def __call__(self, prices):
        return core.BBANDS(prices, period=self.period, nbdev=self.nbdev)


@core.wrap_function(core.KELTNER)
class KELTNER(model.Indicator):
    def __init__(self, period: int = 20, nbatr: float = 2.0):
        self.period = period
        self.nbatr = nbatr

    def __call__(self, prices):
        return core.KELTNER(prices, period=self.period, nbatr=self.nbatr)


@core.wrap_function(core.KER)
class KER(model.Indicator):
    def __init__(self, period: int = 10, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.KER(series, period=self.period, item=self.item)


@core.wrap_function(core.KAMA)
class KAMA(model.Indicator):
    def __init__(self, period: int = 10, fastn: int = 2, slown: int = 30, *, item: str = None):
        self.period = period
        self.fastn = fastn
        self.slown = slown
        self.item = item

    def __call__(self, series):
        return core.KAMA(series, period=self.period, fastn=self.fastn, slown=self.slown, item=self.item)


@core.wrap_function(core.MACD)
class MACD(model.Indicator):
    def __init__(self, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.item = item

    def __call__(self, series):
        return core.MACD(series, n1=self.n1, n2=self.n2, n3=self.n3, item=self.item)


@core.wrap_function(core.PPO)
class PPO(model.Indicator):
    def __init__(self, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.item = item

    def __call__(self, series):
        return core.PPO(series, n1=self.n1, n2=self.n2, n3=self.n3, item=self.item)


@core.wrap_function(core.SLOPE)
class SLOPE(model.Indicator):
    def __init__(self, period: int = 20, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.SLOPE(series, period=self.period, item=self.item)


@core.wrap_function(core.RVALUE)
class RVALUE(model.Indicator):
    def __init__(self, period: int = 20, *, item: str = None):
        self.period = period
        self.item = item

    def __call__(self, series):
        return core.RVALUE(series, period=self.period, item=self.item)


@core.wrap_function(core.FORECAST)
class FORECAST(model.Indicator):
    def __init__(self, period: int = 20, offset: int = 0, *, item: str = None):
        self.period = period
        self.offset = offset
        self.item = item

    def __call__(self, series):
        return core.FORECAST(series, period=self.period, offset=self.offset, item=self.item)


@core.wrap_function(core.STOCH)
class STOCH(model.Indicator):
    def __init__(self, period: int = 14, fastn: int = 3, slown: int = 3):
        self.period = period
        self.fastn = fastn
        self.slown = slown

    def __call__(self, prices):
        return core.STOCH(prices, period=self.period, fastn=self.fastn, slown=self.slown)


@core.wrap_function(core.STREAK)
class STREAK(model.Indicator):
    def __init__(self, *, item: str = None):
        self.item = item

    def __call__(self, series):
        return core.STREAK(series, item=self.item)


@core.wrap_function(core.EVAL)
class EVAL(model.Indicator):
    def __init__(self, expr: str):
        self.expr = expr

    def __call__(self, prices):
        return core.EVAL(prices, expr=self.expr)


__all__ = [name for name in dir() if name.isupper()]
