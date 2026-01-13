"""Expressions Model"""

import inspect

import polars as pl

from polars.datatypes import Struct, Float64

# from typing import Union, TypeAlias
# IntoExpr: TypeAlias = Union[pl.Expr, str, pl.Series]


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
