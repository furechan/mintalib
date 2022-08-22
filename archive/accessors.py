# Do not edit! File generated automatically...

import pandas as pd

from . import core
from . import utils


def register_accessors(name='ta', *, force=False):
    """ Register Pandas Accessors """

    if force or not hasattr(pd.Series, name):
        pd.api.extensions.register_series_accessor(name)(SeriesAccessor)

    if force or not hasattr(pd.DataFrame, name):
        pd.api.extensions.register_dataframe_accessor(name)(PricesAccessor)


class SeriesAccessor:
    """ Pandas Series Accessor """

    def __init__(self, series):
        assert isinstance(series, pd.Series)
        self.series = series

    @utils.wrap_accessor(core.calc_roc)
    def roc(self, period: int = 1):
        series = self.series
        return core.calc_roc(series, period)

    @utils.wrap_accessor(core.calc_diff)
    def diff(self, period: int = 1):
        series = self.series
        return core.calc_diff(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_min)
    def min(self, period: int):
        series = self.series
        return core.calc_min(series, period)

    @utils.wrap_accessor(core.calc_max)
    def max(self, period: int):
        series = self.series
        return core.calc_max(series, period)

    @utils.wrap_accessor(core.calc_sum)
    def sum(self, period: int):
        series = self.series
        return core.calc_sum(series, period)

    @utils.wrap_accessor(core.calc_sma)
    def sma(self, period: int):
        series = self.series
        return core.calc_sma(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_ema)
    def ema(self, period: int, *, mixed: bool = True):
        series = self.series
        return core.calc_ema(series, period, mixed=mixed, wrap=True)

    @utils.wrap_accessor(core.calc_rma)
    def rma(self, period: int):
        series = self.series
        return core.calc_rma(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_wma)
    def wma(self, period: int):
        series = self.series
        return core.calc_wma(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_dema)
    def dema(self, period: int):
        series = self.series
        return core.calc_dema(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_tema)
    def tema(self, period: int = 20):
        series = self.series
        return core.calc_tema(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_ma)
    def ma(self, period: int, *, ma_type: int = 0):
        series = self.series
        return core.calc_ma(series, period, ma_type=ma_type, wrap=True)

    @utils.wrap_accessor(core.calc_rsi)
    def rsi(self, period: int = 14):
        series = self.series
        return core.calc_rsi(series, period)

    @utils.wrap_accessor(core.calc_macd)
    def macd(self, n1: int = 12, n2: int = 26, n3: int = 9):
        series = self.series
        return core.calc_macd(series, n1=n1, n2=n2, n3=n3)

    @utils.wrap_accessor(core.calc_ppo)
    def ppo(self, n1: int = 12, n2: int = 26, n3: int = 9):
        series = self.series
        return core.calc_ppo(series, n1=n1, n2=n2, n3=n3)

    @utils.wrap_accessor(core.calc_slope)
    def slope(self, period: int = 20, option: int = 0, offset: int = 0):
        series = self.series
        return core.calc_slope(series, period, option=option, offset=offset)

    @utils.wrap_accessor(core.calc_curve)
    def curve(self, period: int = 20, option: int = 0, offset: int = 0):
        series = self.series
        return core.calc_curve(series, period, option=option, offset=offset)

    @utils.wrap_accessor(core.calc_stdev)
    def stdev(self, period: int = 20):
        series = self.series
        return core.calc_stdev(series, period)

    @utils.wrap_accessor(core.calc_streak)
    def streak(self):
        series = self.series
        return core.calc_streak(series)


class PricesAccessor:
    """ Pandas Prices Accessor """

    def __init__(self, prices):
        assert isinstance(prices, pd.DataFrame)
        self.prices = prices

    @utils.wrap_accessor(core.calc_avgprice)
    def avgprice(self):
        prices = self.prices
        return core.calc_avgprice(prices)

    @utils.wrap_accessor(core.calc_typprice)
    def typprice(self):
        prices = self.prices
        return core.calc_typprice(prices)

    @utils.wrap_accessor(core.calc_wclprice)
    def wclprice(self):
        prices = self.prices
        return core.calc_wclprice(prices)

    @utils.wrap_accessor(core.calc_midprice)
    def midprice(self):
        prices = self.prices
        return core.calc_midprice(prices)

    @utils.wrap_accessor(core.calc_roc)
    def roc(self, period: int = 1, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_roc(series, period)

    @utils.wrap_accessor(core.calc_diff)
    def diff(self, period: int = 1, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_diff(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_min)
    def min(self, period: int, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_min(series, period)

    @utils.wrap_accessor(core.calc_max)
    def max(self, period: int, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_max(series, period)

    @utils.wrap_accessor(core.calc_sum)
    def sum(self, period: int, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_sum(series, period)

    @utils.wrap_accessor(core.calc_sma)
    def sma(self, period: int, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_sma(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_ema)
    def ema(self, period: int, *, mixed: bool = True, item: str = 'close'):
        series = self.prices[item]
        return core.calc_ema(series, period, mixed=mixed, wrap=True)

    @utils.wrap_accessor(core.calc_rma)
    def rma(self, period: int, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_rma(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_wma)
    def wma(self, period: int, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_wma(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_dema)
    def dema(self, period: int, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_dema(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_tema)
    def tema(self, period: int = 20, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_tema(series, period, wrap=True)

    @utils.wrap_accessor(core.calc_ma)
    def ma(self, period: int, *, ma_type: int = 0, item: str = 'close'):
        series = self.prices[item]
        return core.calc_ma(series, period, ma_type=ma_type, wrap=True)

    @utils.wrap_accessor(core.calc_rsi)
    def rsi(self, period: int = 14, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_rsi(series, period)

    @utils.wrap_accessor(core.calc_plusdi)
    def plusdi(self, period: int = 14):
        prices = self.prices
        return core.calc_plusdi(prices, period)

    @utils.wrap_accessor(core.calc_minusdi)
    def minusdi(self, period: int = 14):
        prices = self.prices
        return core.calc_minusdi(prices, period)

    @utils.wrap_accessor(core.calc_adx)
    def adx(self, period: int = 14):
        prices = self.prices
        return core.calc_adx(prices, period)

    @utils.wrap_accessor(core.calc_trange)
    def trange(self, *, log_prices: bool = False, percent: bool = False):
        prices = self.prices
        return core.calc_trange(prices, log_prices=log_prices, percent=percent, wrap=True)

    @utils.wrap_accessor(core.calc_atr)
    def atr(self, period: int = 14):
        prices = self.prices
        return core.calc_atr(prices, period)

    @utils.wrap_accessor(core.calc_natr)
    def natr(self, period: int = 14):
        prices = self.prices
        return core.calc_natr(prices, period)

    @utils.wrap_accessor(core.calc_latr)
    def latr(self, period: int = 14):
        prices = self.prices
        return core.calc_latr(prices, period)

    @utils.wrap_accessor(core.calc_psar)
    def psar(self, afs: float = 0.02, maxaf: float = 0.2):
        prices = self.prices
        return core.calc_psar(prices, afs=afs, maxaf=maxaf)

    @utils.wrap_accessor(core.calc_bbands)
    def bbands(self, period: int = 20, nbdev: float = 2.0):
        prices = self.prices
        return core.calc_bbands(prices, period, nbdev=nbdev)

    @utils.wrap_accessor(core.calc_keltner)
    def keltner(self, period: int = 20, nbatr: float = 2.0):
        prices = self.prices
        return core.calc_keltner(prices, period, nbatr=nbatr)

    @utils.wrap_accessor(core.calc_macd)
    def macd(self, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_macd(series, n1=n1, n2=n2, n3=n3)

    @utils.wrap_accessor(core.calc_ppo)
    def ppo(self, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_ppo(series, n1=n1, n2=n2, n3=n3)

    @utils.wrap_accessor(core.calc_slope)
    def slope(self, period: int = 20, option: int = 0, offset: int = 0, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_slope(series, period, option=option, offset=offset)

    @utils.wrap_accessor(core.calc_curve)
    def curve(self, period: int = 20, option: int = 0, offset: int = 0, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_curve(series, period, option=option, offset=offset)

    @utils.wrap_accessor(core.calc_stdev)
    def stdev(self, period: int = 20, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_stdev(series, period)

    @utils.wrap_accessor(core.calc_stoch)
    def stoch(self, period: int = 14, fastn: int = 3, slown: int = 3):
        prices = self.prices
        return core.calc_stoch(prices, period, fastn=fastn, slown=slown, wrap=True)

    @utils.wrap_accessor(core.calc_streak)
    def streak(self, *, item: str = 'close'):
        series = self.prices[item]
        return core.calc_streak(series)

