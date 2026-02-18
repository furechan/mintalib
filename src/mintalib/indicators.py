"""
Indicators offer a composable interface where a calculation routine is bound with its parameters.

An indicator instance is a callable and can be applied to prices or series data as if it were a function e.g. `SMA(50)(prices)`.

Indicators also support the `@` operator to apply them to their input data e.g. `SMA(50) @ prices` or to chain them together e.g. `ROC(1) @ EMA(20)`.
"""

# Do not edit! This file was generated.

from mintalib import core
from mintalib.model.indicator import wrap_indicator



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
def SIGN(*, item: str = None): ...

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
