"""Expressions Model"""

import inspect

import polars as pl

from typing import TypeAlias
from polars.datatypes import Struct, Float64


IntoExpr: TypeAlias = pl.Expr | str


def get_series_expr(src):
    if src is None:
        return pl.col("close")
    
    if isinstance(src, str):
        return pl.col(src)
    
    if isinstance(src, pl.Expr):
        return src

    raise ValueError("src must be a string or a Polars Series.")


def get_struct_expr(src):
    if src is None:
        return pl.struct("*")
    
    if isinstance(src, str):
        return pl.struct(src)
    
    if isinstance(src, pl.Expr):
        if src.meta.has_multiple_outputs():
            return pl.struct(src)
        else:
            return src
        
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
            if args and isinstance(args[0], pl.Expr):
                if 'src' in kwargs:
                    raise ValueError("Cannot specify 'src' as a keyword argument when using a positional Polars expression.")
                kwargs['src'] = args[0]
                args = args[1:]

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
