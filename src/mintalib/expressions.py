"""
Polars Expression Factory Methods

Functions in this module are polars expression factories, typically named after
the indicator in upper case as in `SMA`, `EMA`, `MACD`.

The optional `src` keyword parameter allows overriding the default input column.
For series-based indicators the default is `CLOSE` (i.e. `pl.col("close")`).
For price-based indicators `src` is not applicable and should be left as `None`.

Multi-output indicators like `MACD` and `BBANDS` return a polars struct expression
that can be unpacked with `.unnest()`.
"""

# Do not edit! This file was generated.

import polars as pl

from typing import TypeAlias

from mintalib import core
from mintalib.model.expression import wrap_expression

IntoExpr: TypeAlias = pl.Expr | str | None
"""Type alias for polars expressions accepted as inputs (pl.Expr, column name, or None)."""

CLOSE = pl.col('close')
"""Expression for the close price column."""

OHLC = pl.struct(['open', 'high', 'low', 'close'])
"""Expression for open, high, low, close columns as a struct."""



@wrap_expression(core.calc_abs)
def ABS(*, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_adx)
def ADX(period: int = 14, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_alma)
def ALMA(period: int = 9, offset: float = 0.85, sigma: float = 6.0, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_atr)
def ATR(period: int = 14, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_avgprice)
def AVGPRICE(*, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_bbands)
def BBANDS(period: int = 20, nbdev: float = 2.0, *, src: IntoExpr = None) -> tuple: ...

@wrap_expression(core.calc_bbp)
def BBP(period: int = 20, nbdev: float = 2.0, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_bbw)
def BBW(period: int = 20, nbdev: float = 2.0, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_bop)
def BOP(period: int = 20, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_cci)
def CCI(period: int = 20, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_clag)
def CLAG(period: int = 1, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_cmf)
def CMF(period: int = 20, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_crossover)
def CROSSOVER(level: float = 0.0, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_crossunder)
def CROSSUNDER(level: float = 0.0, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_curve)
def CURVE(period: int = 20, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_dema)
def DEMA(period: int, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_diff)
def DIFF(period: int = 1, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_dmi)
def DMI(period: int = 14, *, src: IntoExpr = None) -> tuple: ...

@wrap_expression(core.calc_ema)
def EMA(period: int, *, adjust: bool = False, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_exp)
def EXP(*, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_flag)
def FLAG(*, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_hma)
def HMA(period: int, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_kama)
def KAMA(period: int = 10, fastn: int = 2, slown: int = 30, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_keltner)
def KELTNER(period: int = 20, nbatr: float = 2.0, *, src: IntoExpr = None) -> tuple: ...

@wrap_expression(core.calc_ker)
def KER(period: int = 10, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_lag)
def LAG(period: int, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_log)
def LOG(*, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_lroc)
def LROC(period: int = 1, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_macd)
def MACD(n1: int = 12, n2: int = 26, n3: int = 9, *, src: IntoExpr = None) -> tuple: ...

@wrap_expression(core.calc_macdv)
def MACDV(n1: int = 12, n2: int = 26, n3: int = 9, *, src: IntoExpr = None) -> tuple: ...

@wrap_expression(core.calc_mad)
def MAD(period: int = 14, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_mav)
def MAV(period: int = 20, *, ma_type: str = 'SMA', src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_max)
def MAX(period: int, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_mdi)
def MDI(period: int = 14, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_mfi)
def MFI(period: int = 14, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_midprice)
def MIDPRICE(*, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_min)
def MIN(period: int, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_natr)
def NATR(period: int = 14, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_pdi)
def PDI(period: int = 14, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_ppo)
def PPO(n1: int = 12, n2: int = 26, n3: int = 9, *, src: IntoExpr = None) -> tuple: ...

@wrap_expression(core.calc_price)
def PRICE(item: str = None, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_qsf)
def QSF(period: int = 20, offset: int = 0, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_rma)
def RMA(period: int, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_roc)
def ROC(period: int = 1, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_rsi)
def RSI(period: int = 14, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_rvalue)
def RVALUE(period: int = 20, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_sar)
def SAR(afs: float = 0.02, maxaf: float = 0.2, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_sign)
def SIGN(*, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_slope)
def SLOPE(period: int = 20, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_sma)
def SMA(period: int, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_stdev)
def STDEV(period: int = 20, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_step)
def STEP(threshold: 'float' = 1.0, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_stoch)
def STOCH(period: int = 14, fastn: int = 3, slown: int = 3, *, src: IntoExpr = None) -> tuple: ...

@wrap_expression(core.calc_streak)
def STREAK(*, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_sum)
def SUM(period: int, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_tema)
def TEMA(period: int = 20, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_trange)
def TRANGE(*, log_prices: bool = False, percent: bool = False, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_tsf)
def TSF(period: int = 20, offset: int = 0, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_typprice)
def TYPPRICE(*, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_updown)
def UPDOWN(up_level: float = 0.0, down_level: float = 0.0, *, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_wclprice)
def WCLPRICE(*, src: IntoExpr = None) -> pl.Expr: ...

@wrap_expression(core.calc_wma)
def WMA(period: int, *, src: IntoExpr = None) -> pl.Expr: ...

