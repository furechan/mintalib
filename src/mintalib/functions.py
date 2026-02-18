"""
Calculation functions for technical analysis indicators.

These functions are a thin wrapper arround core calculation routine that handle input and output type conversion.

The function names are all lower case like `sma`, `ema`, etc 
To avoid name conflicts it is advised to import the module as a whole with a short alias like `ta`.
"""

# Do not edit! This file was generated.

from mintalib import core
from mintalib.model.function import wrap_function



@wrap_function(core.calc_abs)
def abs(series): ...

@wrap_function(core.calc_adx)
def adx(prices, period: int = 14): ...

@wrap_function(core.calc_alma)
def alma(series, period: int = 9, offset: float = 0.85, sigma: float = 6.0): ...

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
def clag(series, period: int = 1): ...

@wrap_function(core.calc_cmf)
def cmf(prices, period: int = 20): ...

@wrap_function(core.calc_crossover)
def crossover(series, level: float = 0.0): ...

@wrap_function(core.calc_crossunder)
def crossunder(series, level: float = 0.0): ...

@wrap_function(core.calc_curve)
def curve(series, period: int = 20): ...

@wrap_function(core.calc_dema)
def dema(series, period: int): ...

@wrap_function(core.calc_diff)
def diff(series, period: int = 1): ...

@wrap_function(core.calc_dmi)
def dmi(prices, period: int = 14): ...

@wrap_function(core.calc_ema)
def ema(series, period: int, *, adjust: bool = False): ...

@wrap_function(core.calc_eval)
def eval(prices, expr: str, *, as_flag: bool = False): ...

@wrap_function(core.calc_exp)
def exp(series): ...

@wrap_function(core.calc_flag)
def flag(series): ...

@wrap_function(core.calc_hma)
def hma(series, period: int): ...

@wrap_function(core.calc_kama)
def kama(series, period: int = 10, fastn: int = 2, slown: int = 30): ...

@wrap_function(core.calc_keltner)
def keltner(prices, period: int = 20, nbatr: float = 2.0): ...

@wrap_function(core.calc_ker)
def ker(series, period: int = 10): ...

@wrap_function(core.calc_lag)
def lag(series, period: int): ...

@wrap_function(core.calc_log)
def log(series): ...

@wrap_function(core.calc_lroc)
def lroc(series, period: int = 1): ...

@wrap_function(core.calc_macd)
def macd(series, n1: int = 12, n2: int = 26, n3: int = 9): ...

@wrap_function(core.calc_macdv)
def macdv(prices, n1: int = 12, n2: int = 26, n3: int = 9): ...

@wrap_function(core.calc_mad)
def mad(series, period: int = 14): ...

@wrap_function(core.calc_mav)
def mav(series, period: int = 20, *, ma_type: str = 'SMA'): ...

@wrap_function(core.calc_max)
def max(series, period: int): ...

@wrap_function(core.calc_mdi)
def mdi(prices, period: int = 14): ...

@wrap_function(core.calc_mfi)
def mfi(prices, period: int = 14): ...

@wrap_function(core.calc_midprice)
def midprice(prices): ...

@wrap_function(core.calc_min)
def min(series, period: int): ...

@wrap_function(core.calc_natr)
def natr(prices, period: int = 14): ...

@wrap_function(core.calc_pdi)
def pdi(prices, period: int = 14): ...

@wrap_function(core.calc_ppo)
def ppo(series, n1: int = 12, n2: int = 26, n3: int = 9): ...

@wrap_function(core.calc_price)
def price(prices, item: str = None): ...

@wrap_function(core.calc_qsf)
def qsf(series, period: int = 20, offset: int = 0): ...

@wrap_function(core.calc_rma)
def rma(series, period: int): ...

@wrap_function(core.calc_roc)
def roc(series, period: int = 1): ...

@wrap_function(core.calc_rsi)
def rsi(series, period: int = 14): ...

@wrap_function(core.calc_rvalue)
def rvalue(series, period: int = 20): ...

@wrap_function(core.calc_sar)
def sar(prices, afs: float = 0.02, maxaf: float = 0.2): ...

@wrap_function(core.calc_shift)
def shift(series, period: int): ...

@wrap_function(core.calc_sign)
def sign(series): ...

@wrap_function(core.calc_slope)
def slope(series, period: int = 20): ...

@wrap_function(core.calc_sma)
def sma(series, period: int): ...

@wrap_function(core.calc_stdev)
def stdev(series, period: int = 20): ...

@wrap_function(core.calc_step)
def step(series, threshold: 'float' = 1.0): ...

@wrap_function(core.calc_stoch)
def stoch(prices, period: int = 14, fastn: int = 3, slown: int = 3): ...

@wrap_function(core.calc_streak)
def streak(series): ...

@wrap_function(core.calc_sum)
def sum(series, period: int): ...

@wrap_function(core.calc_tema)
def tema(series, period: int = 20): ...

@wrap_function(core.calc_trange)
def trange(prices, *, log_prices: bool = False, percent: bool = False): ...

@wrap_function(core.calc_tsf)
def tsf(series, period: int = 20, offset: int = 0): ...

@wrap_function(core.calc_typprice)
def typprice(prices): ...

@wrap_function(core.calc_updown)
def updown(series, up_level: float = 0.0, down_level: float = 0.0): ...

@wrap_function(core.calc_wclprice)
def wclprice(prices): ...

@wrap_function(core.calc_wma)
def wma(series, period: int): ...

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
