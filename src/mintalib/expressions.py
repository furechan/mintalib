"""Expressions Module"""

# PREAMBLE Do not edit! This file was generated

import inspect

import polars as pl

from polars.datatypes import Struct, Float64

from . import core

from typing import Union, TypeAlias


IntoExpr: TypeAlias = Union[pl.Expr, str, pl.Series]

nan = float('nan')


def get_series_expr(src):
    if isinstance(src, str):
        return pl.col(src)
    elif isinstance(src, pl.Expr):
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


def wrap_expression(calc_func):
    calc_sig = inspect.signature(calc_func)
    first_param = next(iter(calc_sig.parameters.values()))
    force_struct = first_param.name == 'prices'

    def decorator(func):
        name = func.__name__.lower()
        metadata = getattr(calc_func, 'metadata', {})
        output_names = metadata.get('output_names', ())
        output_type = Struct({n: Float64 for n in output_names}) if output_names else Float64
        signature = inspect.signature(func)

        def wrapper(*args, **kwargs):
            bound_args = signature.bind(*args, **kwargs)
            args, kwargs = (), dict(bound_args.arguments)

            src = kwargs.pop('src', None)

            if force_struct:
                source = get_struct_expr(src)
            else:
                source = get_series_expr(src)

            def batch_func(prices):
                if force_struct:
                    prices = prices.struct.unnest()

                output = calc_func(prices, *args, **kwargs)
                
                if isinstance(output, tuple):
                    return pl.DataFrame(output._asdict()).fill_nan(None).to_struct()
                else:
                    return pl.Series(output).fill_nan(None)
            
            expr = source.map_batches(batch_func, return_dtype=output_type).alias(name)
#            expr = expr.struct.unnest() if output_names else expr.alias(name)
            
            return expr
        
        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__doc__ = calc_func.__doc__
        wrapper.__signature__ = signature

        return wrapper
    
    return decorator

@wrap_expression(core.calc_abs)
def ABS(src): ...


@wrap_expression(core.calc_adx)
def ADX(period: int = 14, *, src='*'): ...


@wrap_expression(core.calc_alma)
def ALMA(src, period: int = 9, offset: float = 0.85, sigma: float = 6.0): ...


@wrap_expression(core.calc_atr)
def ATR(period: int = 14, *, src='*'): ...


@wrap_expression(core.calc_avgprice)
def AVGPRICE(*, src='*'): ...


@wrap_expression(core.calc_bbands)
def BBANDS(period: int = 20, nbdev: float = 2.0, *, src='*'): ...


@wrap_expression(core.calc_bop)
def BOP(period: int = 20, *, src='*'): ...


@wrap_expression(core.calc_cci)
def CCI(period: int = 20, *, src='*'): ...


@wrap_expression(core.calc_clag)
def CLAG(src, period: int = 1): ...


@wrap_expression(core.calc_cmf)
def CMF(period: int = 20, *, src='*'): ...


@wrap_expression(core.calc_crossover)
def CROSSOVER(src, level: float = 0.0): ...


@wrap_expression(core.calc_crossunder)
def CROSSUNDER(src, level: float = 0.0): ...


@wrap_expression(core.calc_curve)
def CURVE(src, period: int = 20): ...


@wrap_expression(core.calc_dema)
def DEMA(src, period: int): ...


@wrap_expression(core.calc_diff)
def DIFF(src, period: int = 1): ...


@wrap_expression(core.calc_dmi)
def DMI(period: int = 14, *, src='*'): ...


@wrap_expression(core.calc_ema)
def EMA(src, period: int, *, adjust: bool = False): ...


@wrap_expression(core.calc_exp)
def EXP(src): ...


@wrap_expression(core.calc_flag)
def FLAG(src): ...


@wrap_expression(core.calc_hma)
def HMA(src, period: int): ...


@wrap_expression(core.calc_kama)
def KAMA(src, period: int = 10, fastn: int = 2, slown: int = 30): ...


@wrap_expression(core.calc_keltner)
def KELTNER(period: int = 20, nbatr: float = 2.0, *, src='*'): ...


@wrap_expression(core.calc_ker)
def KER(src, period: int = 10): ...


@wrap_expression(core.calc_lag)
def LAG(src, period: int): ...


@wrap_expression(core.calc_log)
def LOG(src): ...


@wrap_expression(core.calc_lroc)
def LROC(src, period: int = 1): ...


@wrap_expression(core.calc_macd)
def MACD(src, n1: int = 12, n2: int = 26, n3: int = 9): ...


@wrap_expression(core.calc_mad)
def MAD(src, period: int = 14): ...


@wrap_expression(core.calc_mav)
def MAV(src, period: int = 20, *, ma_type: str = 'SMA'): ...


@wrap_expression(core.calc_max)
def MAX(src, period: int): ...


@wrap_expression(core.calc_mdi)
def MDI(period: int = 14, *, src='*'): ...


@wrap_expression(core.calc_mfi)
def MFI(period: int = 14, *, src='*'): ...


@wrap_expression(core.calc_midprice)
def MIDPRICE(*, src='*'): ...


@wrap_expression(core.calc_min)
def MIN(src, period: int): ...


@wrap_expression(core.calc_natr)
def NATR(period: int = 14, *, src='*'): ...


@wrap_expression(core.calc_pdi)
def PDI(period: int = 14, *, src='*'): ...


@wrap_expression(core.calc_ppo)
def PPO(src, n1: int = 12, n2: int = 26, n3: int = 9): ...


@wrap_expression(core.calc_price)
def PRICE(item: str = None, *, src='*'): ...


@wrap_expression(core.calc_qsf)
def QSF(src, period: int = 20, offset: int = 0): ...


@wrap_expression(core.calc_rma)
def RMA(src, period: int): ...


@wrap_expression(core.calc_roc)
def ROC(src, period: int = 1): ...


@wrap_expression(core.calc_rsi)
def RSI(src, period: int = 14): ...


@wrap_expression(core.calc_rvalue)
def RVALUE(src, period: int = 20): ...


@wrap_expression(core.calc_sar)
def SAR(afs: float = 0.02, maxaf: float = 0.2, *, src='*'): ...


@wrap_expression(core.calc_shift)
def SHIFT(src, period: int): ...


@wrap_expression(core.calc_sign)
def SIGN(src, na_value: float = nan): ...


@wrap_expression(core.calc_slope)
def SLOPE(src, period: int = 20): ...


@wrap_expression(core.calc_sma)
def SMA(src, period: int): ...


@wrap_expression(core.calc_stdev)
def STDEV(src, period: int = 20): ...


@wrap_expression(core.calc_step)
def STEP(src, threshold: 'float' = 1.0): ...


@wrap_expression(core.calc_stoch)
def STOCH(period: int = 14, fastn: int = 3, slown: int = 3, *, src='*'): ...


@wrap_expression(core.calc_streak)
def STREAK(src): ...


@wrap_expression(core.calc_sum)
def SUM(src, period: int): ...


@wrap_expression(core.calc_tema)
def TEMA(src, period: int = 20): ...


@wrap_expression(core.calc_trange)
def TRANGE(*, log_prices: bool = False, percent: bool = False, src='*'): ...


@wrap_expression(core.calc_tsf)
def TSF(src, period: int = 20, offset: int = 0): ...


@wrap_expression(core.calc_typprice)
def TYPPRICE(*, src='*'): ...


@wrap_expression(core.calc_updown)
def UPDOWN(src, up_level: float = 0.0, down_level: float = 0.0): ...


@wrap_expression(core.calc_wclprice)
def WCLPRICE(*, src='*'): ...


@wrap_expression(core.calc_wma)
def WMA(src, period: int): ...


__all__ = [
    'ABS', 'ADX', 'ALMA', 'ATR', 'AVGPRICE', 'BBANDS', 'BOP', 'CCI',
    'CLAG', 'CMF', 'CROSSOVER', 'CROSSUNDER', 'CURVE', 'DEMA', 'DIFF',
    'DMI', 'EMA', 'EXP', 'FLAG', 'HMA', 'KAMA', 'KELTNER', 'KER', 'LAG',
    'LOG', 'LROC', 'MACD', 'MAD', 'MAV', 'MAX', 'MDI', 'MFI', 'MIDPRICE',
    'MIN', 'NATR', 'PDI', 'PPO', 'PRICE', 'QSF', 'RMA', 'ROC', 'RSI',
    'RVALUE', 'SAR', 'SHIFT', 'SIGN', 'SLOPE', 'SMA', 'STDEV', 'STEP',
    'STOCH', 'STREAK', 'SUM', 'TEMA', 'TRANGE', 'TSF', 'TYPPRICE',
    'UPDOWN', 'WCLPRICE', 'WMA'
]
