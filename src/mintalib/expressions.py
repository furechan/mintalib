"""Expressions Module"""

# PREAMBLE Do not edit! This file was generated

import polars as pl

from polars.datatypes import Struct, Float64

from . import core

from typing import Union, TypeAlias

from functools import wraps


IntoExpr: TypeAlias = Union[pl.Expr, str, pl.Series]

nan = float('nan')


def get_series_expr(src):
    if isinstance(src, str):
        return pl.col(src)
    elif isinstance(src, pl.Series):
        return src
    else:
        raise ValueError("src must be a string or a Polars Series.")


def get_struct_expr(src):
    if src is None:
        return pl.struct("*")
    
    if isinstance(src, str):
        return pl.col(src).struct
    
    if isinstance(src, pl.Expr):
        return pl.struct(src)
        
    raise ValueError(f"Unsupported src type: {type(src)}")



def series_expression(calc_func):
    def decorator(func):
        name = func.__name__.lower()
        metadata = getattr(calc_func, 'metadata', {})
        output_names = metadata.get('output_names', ())
        output_type = Struct({n: Float64 for n in output_names}) if output_names else Float64
        
        @wraps(func)
        def wrapper(src, *args, **kwargs):
            print(f"Calling {func.__name__} with src={src}, args={args}, kwargs={kwargs}")
            source = get_series_expr(src)

            def batch_func(series):
                output = calc_func(series, *args, **kwargs)
                if output_names:
                    return pl.DataFrame(output._asdict()).to_struct(name)
                return output
            
            expr = source.map_batches(batch_func, return_dtype=output_type)
            expr = expr.struct.unnest() if output_names else expr.alias(name)

            return expr
             
        return wrapper
    return decorator


def prices_expression(calc_func):
    def decorator(func):
        name = func.__name__.lower()
        metadata = getattr(calc_func, 'metadata', {})
        output_names = metadata.get('output_names', ())
        output_type = Struct({n: Float64 for n in output_names}) if output_names else Float64
        
        @wraps(func)
        def wrapper(*args, src=None, **kwargs):
            print(f"Calling {func.__name__} with src={src}, args={args}, kwargs={kwargs}")
            source = get_struct_expr(src)

            def batch_func(prices):
                output = calc_func(prices.struct, *args, **kwargs)
                if output_names:
                    return pl.DataFrame(output._asdict()).to_struct(name)
                return output
            
            expr = source.map_batches(batch_func, return_dtype=output_type)
            expr = expr.struct.unnest() if output_names else expr.alias(name)
            
            return expr
        
        return wrapper
    return decorator

@series_expression(core.calc_abs)
def ABS(src): ...


@prices_expression(core.calc_adx)
def ADX(period: int = 14, *, src='*'): ...


@series_expression(core.calc_alma)
def ALMA(src, period: int = 9, offset: float = 0.85, sigma: float = 6.0): ...


@prices_expression(core.calc_atr)
def ATR(period: int = 14, *, src='*'): ...


@prices_expression(core.calc_avgprice)
def AVGPRICE(*, src='*'): ...


@prices_expression(core.calc_bbands)
def BBANDS(period: int = 20, nbdev: float = 2.0, *, src='*'): ...


@prices_expression(core.calc_bop)
def BOP(period: int = 20, *, src='*'): ...


@prices_expression(core.calc_cci)
def CCI(period: int = 20, *, src='*'): ...


@series_expression(core.calc_clag)
def CLAG(src, period: int = 1): ...


@prices_expression(core.calc_cmf)
def CMF(period: int = 20, *, src='*'): ...


@series_expression(core.calc_crossover)
def CROSSOVER(src, level: float = 0.0): ...


@series_expression(core.calc_crossunder)
def CROSSUNDER(src, level: float = 0.0): ...


@series_expression(core.calc_curve)
def CURVE(src, period: int = 20): ...


@series_expression(core.calc_dema)
def DEMA(src, period: int): ...


@series_expression(core.calc_diff)
def DIFF(src, period: int = 1): ...


@prices_expression(core.calc_dmi)
def DMI(period: int = 14, *, src='*'): ...


@series_expression(core.calc_ema)
def EMA(src, period: int, *, adjust: bool = False): ...


@prices_expression(core.calc_eval)
def EVAL(expr: str, *, as_flag: bool = False, src='*'): ...


@series_expression(core.calc_exp)
def EXP(src): ...


@series_expression(core.calc_flag)
def FLAG(src): ...


@series_expression(core.calc_hma)
def HMA(src, period: int): ...


@series_expression(core.calc_kama)
def KAMA(src, period: int = 10, fastn: int = 2, slown: int = 30): ...


@prices_expression(core.calc_keltner)
def KELTNER(period: int = 20, nbatr: float = 2.0, *, src='*'): ...


@series_expression(core.calc_ker)
def KER(src, period: int = 10): ...


@series_expression(core.calc_lag)
def LAG(src, period: int): ...


@series_expression(core.calc_log)
def LOG(src): ...


@series_expression(core.calc_lroc)
def LROC(src, period: int = 1): ...


@series_expression(core.calc_macd)
def MACD(src, n1: int = 12, n2: int = 26, n3: int = 9): ...


@series_expression(core.calc_mad)
def MAD(src, period: int = 14): ...


@series_expression(core.calc_mav)
def MAV(src, period: int = 20, *, ma_type: str = 'SMA'): ...


@series_expression(core.calc_max)
def MAX(src, period: int): ...


@prices_expression(core.calc_mdi)
def MDI(period: int = 14, *, src='*'): ...


@prices_expression(core.calc_mfi)
def MFI(period: int = 14, *, src='*'): ...


@prices_expression(core.calc_midprice)
def MIDPRICE(*, src='*'): ...


@series_expression(core.calc_min)
def MIN(src, period: int): ...


@prices_expression(core.calc_natr)
def NATR(period: int = 14, *, src='*'): ...


@prices_expression(core.calc_pdi)
def PDI(period: int = 14, *, src='*'): ...


@series_expression(core.calc_ppo)
def PPO(src, n1: int = 12, n2: int = 26, n3: int = 9): ...


@prices_expression(core.calc_price)
def PRICE(item: str = None, *, src='*'): ...


@series_expression(core.calc_qsf)
def QSF(src, period: int = 20, offset: int = 0): ...


@series_expression(core.calc_rma)
def RMA(src, period: int): ...


@series_expression(core.calc_roc)
def ROC(src, period: int = 1): ...


@series_expression(core.calc_rsi)
def RSI(src, period: int = 14): ...


@series_expression(core.calc_rvalue)
def RVALUE(src, period: int = 20): ...


@prices_expression(core.calc_sar)
def SAR(afs: float = 0.02, maxaf: float = 0.2, *, src='*'): ...


@series_expression(core.calc_shift)
def SHIFT(src, period: int): ...


@series_expression(core.calc_sign)
def SIGN(src, na_value: float = nan): ...


@series_expression(core.calc_slope)
def SLOPE(src, period: int = 20): ...


@series_expression(core.calc_sma)
def SMA(src, period: int): ...


@series_expression(core.calc_stdev)
def STDEV(src, period: int = 20): ...


@series_expression(core.calc_step)
def STEP(src, threshold: 'float' = 1.0): ...


@prices_expression(core.calc_stoch)
def STOCH(period: int = 14, fastn: int = 3, slown: int = 3, *, src='*'): ...


@series_expression(core.calc_streak)
def STREAK(src): ...


@series_expression(core.calc_sum)
def SUM(src, period: int): ...


@series_expression(core.calc_tema)
def TEMA(src, period: int = 20): ...


@prices_expression(core.calc_trange)
def TRANGE(*, log_prices: bool = False, percent: bool = False, src='*'): ...


@series_expression(core.calc_tsf)
def TSF(src, period: int = 20, offset: int = 0): ...


@prices_expression(core.calc_typprice)
def TYPPRICE(*, src='*'): ...


@series_expression(core.calc_updown)
def UPDOWN(src, up_level: float = 0.0, down_level: float = 0.0): ...


@prices_expression(core.calc_wclprice)
def WCLPRICE(*, src='*'): ...


@series_expression(core.calc_wma)
def WMA(src, period: int): ...


__all__ = [
    'ABS', 'ADX', 'ALMA', 'ATR', 'AVGPRICE', 'BBANDS', 'BOP', 'CCI',
    'CLAG', 'CMF', 'CROSSOVER', 'CROSSUNDER', 'CURVE', 'DEMA', 'DIFF',
    'DMI', 'EMA', 'EVAL', 'EXP', 'FLAG', 'HMA', 'KAMA', 'KELTNER', 'KER',
    'LAG', 'LOG', 'LROC', 'MACD', 'MAD', 'MAV', 'MAX', 'MDI', 'MFI',
    'MIDPRICE', 'MIN', 'NATR', 'PDI', 'PPO', 'PRICE', 'QSF', 'RMA', 'ROC',
    'RSI', 'RVALUE', 'SAR', 'SHIFT', 'SIGN', 'SLOPE', 'SMA', 'STDEV',
    'STEP', 'STOCH', 'STREAK', 'SUM', 'TEMA', 'TRANGE', 'TSF', 'TYPPRICE',
    'UPDOWN', 'WCLPRICE', 'WMA'
]
