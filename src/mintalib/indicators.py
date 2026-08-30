# ty: ignore[empty-body] (decorator-replaces-body pattern: empty stubs are intentional)
"""
Indicators offer a composable interface where a calculation routine is bound with its parameters.

This module is pandas-only: indicators accept pandas DataFrames, pandas Series, or numpy arrays,
and return pandas results.

An indicator instance is a callable applied to prices or series data: `SMA(50)(prices)`.

Series-output indicators chain through the `|` operator: `EMA(20) | ROC(1)`.

Single-output indicators return a pandas Series; multi-output indicators (e.g. `MACD`, `BBANDS`) return a DataFrame.
Select one output of a multi-output indicator as a series indicator with `MACD()["macd"]`.
"""

# Do not edit! This file was generated.
from mintalib import core
from mintalib.model.indicator import (
    PricesToFrame,
    PricesToSeries,
    SeriesToFrame,
    SeriesToSeries,
    wrap_indicator,
)



@wrap_indicator(core.calc_abs)
def ABS(*, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_adx)
def ADX(period: int = 14) -> PricesToSeries: ...

@wrap_indicator(core.calc_alma)
def ALMA(period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_atr)
def ATR(period: int = 14) -> PricesToSeries: ...

@wrap_indicator(core.calc_avgprice)
def AVGPRICE() -> PricesToSeries: ...

@wrap_indicator(core.calc_bbands)
def BBANDS(period: int = 20, nbdev: float = 2.0, *, item: str | None = None) -> SeriesToFrame: ...

@wrap_indicator(core.calc_bbp)
def BBP(period: int = 20, nbdev: float = 2.0, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_bbw)
def BBW(period: int = 20, nbdev: float = 2.0, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_bop)
def BOP() -> PricesToSeries: ...

@wrap_indicator(core.calc_cci)
def CCI(period: int = 20) -> PricesToSeries: ...

@wrap_indicator(core.calc_clag)
def CLAG(period: int = 1, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_cmf)
def CMF(period: int = 20) -> PricesToSeries: ...

@wrap_indicator(core.calc_crossover)
def CROSSOVER(level: float = 0.0, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_crossunder)
def CROSSUNDER(level: float = 0.0, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_dema)
def DEMA(period: int, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_diff)
def DIFF(period: int = 1, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_dmi)
def DMI(period: int = 14) -> PricesToFrame: ...

@wrap_indicator(core.calc_donchian)
def DONCHIAN(period: int = 20) -> PricesToFrame: ...

@wrap_indicator(core.calc_ema)
def EMA(period: int, *, adjust: bool = False, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_exp)
def EXP(*, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_flag)
def FLAG(*, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_hma)
def HMA(period: int, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_kama)
def KAMA(period: int = 10, fastn: int = 2, slown: int = 30, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_keltner)
def KELTNER(period: int = 20, nbatr: float = 2.0) -> PricesToFrame: ...

@wrap_indicator(core.calc_ker)
def KER(period: int = 10, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_lag)
def LAG(period: int, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_linreg)
def LINREG(period: int = 20, offset: int = 0, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_linreg_rmse)
def LINREG_RMSE(period: int = 20, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_linreg_rvalue)
def LINREG_RVALUE(period: int = 20, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_linreg_slope)
def LINREG_SLOPE(period: int = 20, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_log)
def LOG(*, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_lroc)
def LROC(period: int = 1, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_macd)
def MACD(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str | None = None) -> SeriesToFrame: ...

@wrap_indicator(core.calc_macdv)
def MACDV(n1: int = 12, n2: int = 26, n3: int = 9) -> PricesToFrame: ...

@wrap_indicator(core.calc_mad)
def MAD(period: int = 14, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_mav)
def MAV(period: int = 20, *, matype: str = 'sma', item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_max)
def MAX(period: int, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_mdi)
def MDI(period: int = 14) -> PricesToSeries: ...

@wrap_indicator(core.calc_medprice)
def MEDPRICE() -> PricesToSeries: ...

@wrap_indicator(core.calc_mfi)
def MFI(period: int = 14) -> PricesToSeries: ...

@wrap_indicator(core.calc_min)
def MIN(period: int, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_natr)
def NATR(period: int = 14) -> PricesToSeries: ...

@wrap_indicator(core.calc_obv)
def OBV() -> PricesToSeries: ...

@wrap_indicator(core.calc_pdi)
def PDI(period: int = 14) -> PricesToSeries: ...

@wrap_indicator(core.calc_ppo)
def PPO(n1: int = 12, n2: int = 26, n3: int = 9, *, item: str | None = None) -> SeriesToFrame: ...

@wrap_indicator(core.calc_price)
def PRICE(item: str | None = None) -> PricesToSeries: ...

@wrap_indicator(core.calc_quadreg)
def QUADREG(period: int = 20, offset: int = 0, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_quadreg_curve)
def QUADREG_CURVE(period: int = 20, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_quadreg_rmse)
def QUADREG_RMSE(period: int = 20, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_quadreg_rvalue)
def QUADREG_RVALUE(period: int = 20, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_quadreg_slope)
def QUADREG_SLOPE(period: int = 20, offset: int = 0, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_rma)
def RMA(period: int, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_roc)
def ROC(period: int = 1, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_rocp)
def ROCP(period: int = 1, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_rsi)
def RSI(period: int = 14, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_sar)
def SAR(afs: float = 0.02, maxaf: float = 0.2) -> PricesToSeries: ...

@wrap_indicator(core.calc_sign)
def SIGN(*, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_sma)
def SMA(period: int, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_stdev)
def STDEV(period: int = 20, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_step)
def STEP(threshold: float = 1.0, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_stoch)
def STOCH(period: int = 14, fastn: int = 3, slown: int = 3) -> PricesToFrame: ...

@wrap_indicator(core.calc_streak)
def STREAK(*, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_sum)
def SUM(period: int, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_tema)
def TEMA(period: int = 20, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_trange)
def TRANGE(*, log_prices: bool = False, percent: bool = False) -> PricesToSeries: ...

@wrap_indicator(core.calc_typprice)
def TYPPRICE() -> PricesToSeries: ...

@wrap_indicator(core.calc_updown)
def UPDOWN(up_level: float = 0.0, down_level: float = 0.0, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_wclprice)
def WCLPRICE() -> PricesToSeries: ...

@wrap_indicator(core.calc_wma)
def WMA(period: int, *, item: str | None = None) -> SeriesToSeries: ...

@wrap_indicator(core.calc_zlema)
def ZLEMA(period: int, *, item: str | None = None) -> SeriesToSeries: ...

__all__ = [
    'ABS', 'ADX', 'ALMA', 'ATR', 'AVGPRICE', 'BBANDS', 'BBP', 'BBW', 'BOP',
    'CCI', 'CLAG', 'CMF', 'CROSSOVER', 'CROSSUNDER', 'DEMA', 'DIFF', 'DMI',
    'DONCHIAN', 'EMA', 'EXP', 'FLAG', 'HMA', 'KAMA', 'KELTNER', 'KER',
    'LAG', 'LINREG', 'LINREG_RMSE', 'LINREG_RVALUE', 'LINREG_SLOPE', 'LOG',
    'LROC', 'MACD', 'MACDV', 'MAD', 'MAV', 'MAX', 'MDI', 'MEDPRICE', 'MFI',
    'MIN', 'NATR', 'OBV', 'PDI', 'PPO', 'PRICE', 'QUADREG',
    'QUADREG_CURVE', 'QUADREG_RMSE', 'QUADREG_RVALUE', 'QUADREG_SLOPE',
    'RMA', 'ROC', 'ROCP', 'RSI', 'SAR', 'SIGN', 'SMA', 'STDEV', 'STEP',
    'STOCH', 'STREAK', 'SUM', 'TEMA', 'TRANGE', 'TYPPRICE', 'UPDOWN',
    'WCLPRICE', 'WMA', 'ZLEMA'
]
