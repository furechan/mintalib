# ty: ignore[empty-body] (decorator-replaces-body pattern: empty stubs are intentional)
"""
Polars Expression Factory Methods

Functions in this module are polars expression factories, typically named after
the indicator in upper case as in `SMA`, `EMA`, `MACD`.

This module is polars-only: factories build native polars expressions for use in
`select` or `with_columns` contexts. For pandas, use `mintalib.indicators` or `mintalib.functions`.

The optional `src` keyword parameter allows overriding the default input column.
For series-based indicators the default is the `close` column.
Price-based indicators use semantic keyword sources such as `high=`, `low=`,
`close=`, and `volume=`, defaulting to columns with those names.

Multi-output indicators like `MACD` and `BBANDS` return a polars struct expression
that can be unpacked with `.unnest()`.
"""

# Do not edit! This file was generated.

import polars as pl

from mintalib import core
from mintalib.model.expression import (
    CLOSE as CLOSE,
    ExprBundle as ExprBundle,
    OHLC as OHLC,
    IntoExpr,
)


from mintalib.model.expression import (
    wrap_columns_expression,
    wrap_series_expression,
)

@wrap_series_expression(core.calc_abs)
def ABS(*, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_adx)
def ADX(period: int = 14, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_alma)
def ALMA(period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_atr)
def ATR(period: int = 14, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_avgprice)
def AVGPRICE(*, open: IntoExpr = 'open', high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_bbands)
def BBANDS(period: int = 20, nbdev: float = 2.0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_bbp)
def BBP(period: int = 20, nbdev: float = 2.0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_bbw)
def BBW(period: int = 20, nbdev: float = 2.0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_bop)
def BOP(*, open: IntoExpr = 'open', high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_cci)
def CCI(period: int = 20, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_clag)
def CLAG(period: int = 1, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_cmf)
def CMF(period: int = 20, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close', volume: IntoExpr = 'volume') -> pl.Expr: ...

@wrap_series_expression(core.calc_crossover)
def CROSSOVER(level: float = 0.0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_crossunder)
def CROSSUNDER(level: float = 0.0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_dema)
def DEMA(period: int, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_diff)
def DIFF(period: int = 1, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_dmi)
def DMI(period: int = 14, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_donchian)
def DONCHIAN(period: int = 20, *, high: IntoExpr = 'high', low: IntoExpr = 'low') -> pl.Expr: ...

@wrap_series_expression(core.calc_ema)
def EMA(period: int, *, adjust: bool = False, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_exp)
def EXP(*, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_flag)
def FLAG(*, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_hma)
def HMA(period: int, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_kama)
def KAMA(period: int = 10, fastn: int = 2, slown: int = 30, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_keltner)
def KELTNER(period: int = 20, nbatr: float = 2.0, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_ker)
def KER(period: int = 10, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_lag)
def LAG(period: int, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_linreg)
def LINREG(period: int = 20, offset: int = 0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_linreg_rmse)
def LINREG_RMSE(period: int = 20, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_linreg_rvalue)
def LINREG_RVALUE(period: int = 20, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_linreg_slope)
def LINREG_SLOPE(period: int = 20, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_log)
def LOG(*, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_lroc)
def LROC(period: int = 1, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_macd)
def MACD(n1: int = 12, n2: int = 26, n3: int = 9, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_macdv)
def MACDV(n1: int = 12, n2: int = 26, n3: int = 9, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_mad)
def MAD(period: int = 14, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_mav)
def MAV(period: int = 20, *, matype: str = 'sma', src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_max)
def MAX(period: int, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_mdi)
def MDI(period: int = 14, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_medprice)
def MEDPRICE(*, high: IntoExpr = 'high', low: IntoExpr = 'low') -> pl.Expr: ...

@wrap_columns_expression(core.calc_mfi)
def MFI(period: int = 14, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close', volume: IntoExpr = 'volume') -> pl.Expr: ...

@wrap_series_expression(core.calc_min)
def MIN(period: int, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_natr)
def NATR(period: int = 14, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_obv)
def OBV(*, close: IntoExpr = 'close', volume: IntoExpr = 'volume') -> pl.Expr: ...

@wrap_columns_expression(core.calc_pdi)
def PDI(period: int = 14, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_ppo)
def PPO(n1: int = 12, n2: int = 26, n3: int = 9, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_quadreg)
def QUADREG(period: int = 20, offset: int = 0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_quadreg_curve)
def QUADREG_CURVE(period: int = 20, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_quadreg_rmse)
def QUADREG_RMSE(period: int = 20, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_quadreg_rvalue)
def QUADREG_RVALUE(period: int = 20, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_quadreg_slope)
def QUADREG_SLOPE(period: int = 20, offset: int = 0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_rma)
def RMA(period: int, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_roc)
def ROC(period: int = 1, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_rocp)
def ROCP(period: int = 1, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_rsi)
def RSI(period: int = 14, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_sar)
def SAR(afs: float = 0.02, maxaf: float = 0.2, *, high: IntoExpr = 'high', low: IntoExpr = 'low') -> pl.Expr: ...

@wrap_series_expression(core.calc_sign)
def SIGN(*, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_sma)
def SMA(period: int, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_stdev)
def STDEV(period: int = 20, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_step)
def STEP(threshold: float = 1.0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_stoch)
def STOCH(period: int = 14, fastn: int = 3, slown: int = 3, *, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_streak)
def STREAK(*, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_sum)
def SUM(period: int, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_tema)
def TEMA(period: int = 20, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_trange)
def TRANGE(*, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_typprice)
def TYPPRICE(*, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_updown)
def UPDOWN(up_level: float = 0.0, down_level: float = 0.0, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_columns_expression(core.calc_wclprice)
def WCLPRICE(*, high: IntoExpr = 'high', low: IntoExpr = 'low', close: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_wma)
def WMA(period: int, *, src: IntoExpr = 'close') -> pl.Expr: ...

@wrap_series_expression(core.calc_zlema)
def ZLEMA(period: int, *, src: IntoExpr = 'close') -> pl.Expr: ...

__all__ = [
    'ABS', 'ADX', 'ALMA', 'ATR', 'AVGPRICE', 'BBANDS', 'BBP', 'BBW', 'BOP',
    'CCI', 'CLAG', 'CMF', 'CROSSOVER', 'CROSSUNDER', 'DEMA', 'DIFF', 'DMI',
    'DONCHIAN', 'EMA', 'EXP', 'ExprBundle', 'FLAG', 'HMA', 'KAMA',
    'KELTNER', 'KER', 'LAG', 'LINREG', 'LINREG_RMSE', 'LINREG_RVALUE',
    'LINREG_SLOPE', 'LOG', 'LROC', 'MACD', 'MACDV', 'MAD', 'MAV', 'MAX',
    'MDI', 'MEDPRICE', 'MFI', 'MIN', 'NATR', 'OBV', 'PDI', 'PPO',
    'QUADREG', 'QUADREG_CURVE', 'QUADREG_RMSE', 'QUADREG_RVALUE',
    'QUADREG_SLOPE', 'RMA', 'ROC', 'ROCP', 'RSI', 'SAR', 'SIGN', 'SMA',
    'STDEV', 'STEP', 'STOCH', 'STREAK', 'SUM', 'TEMA', 'TRANGE',
    'TYPPRICE', 'UPDOWN', 'WCLPRICE', 'WMA', 'ZLEMA'
]
