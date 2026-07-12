"""Expressions Model"""

import inspect

import polars as pl

from typing import TypeAlias, ParamSpec, Callable, Any, Protocol, overload
from polars.datatypes import Struct, Float64


IntoExpr: TypeAlias = pl.Expr | str

P = ParamSpec("P")


class ExprFactory(Protocol[P]):
    """
    Call signature of wrapped expression factories.

    Wrapped factories accept an optional leading polars expression as `src`,
    so they compose with `Expr.pipe` as in `EMA(20).pipe(ROC, 1)`.
    """

    @overload
    def __call__(self, src: pl.Expr, /, *args: P.args, **kwargs: P.kwargs) -> pl.Expr: ...
    @overload
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> pl.Expr: ...



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


def wrap_expression(calc_func) -> Callable[[Callable[P, Any]], ExprFactory[P]]:
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
                
                asdict = getattr(output, "_asdict", None)
                if asdict is not None:
                    return pl.DataFrame(asdict(), nan_to_null=True).to_struct()
                else:
                    return pl.Series(output, nan_to_null=True)
            
            return source.map_batches(batch_func, return_dtype=output_type).alias(name)
        
        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__module__ = func.__module__
        wrapper.__doc__ = calc_func.__doc__
        wrapper.__signature__ = signature  # ty: ignore[unresolved-attribute]

        return wrapper

    return decorator
