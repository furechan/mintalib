import inspect

import polars as pl
from polars.datatypes import Struct, Float64

import numpy as np

NAMESPACE = "ts"

OPEN = pl.col('open')
HIGH = pl.col('high')
LOW = pl.col('low')
CLOSE = pl.col('close')
OHLC = pl.struct(['open', 'high', 'low', 'close'])

__all__ = "OPEN", "HIGH", "LOW", "CLOSE", "OHLC"


def wrap_polars(result, name: str):
    """ wrap result to polars """

    if isinstance(result, tuple) and hasattr(result, '_asdict'):
        result = result._asdict()

    if isinstance(result, dict):
        return pl.DataFrame(result).to_struct(name=name)

    if isinstance(result, np.ndarray):
        return pl.Series(values=result, name=name)

    return result



def expression_method(func):
    name = func.__name__
    name = name.removeprefix("calc_")

    metadata = getattr(func, 'metadata', {})
    output_names = metadata.get('output_names', ())
    output_type = Struct({n: Float64 for n in output_names}) if output_names else Float64
 
    signature = inspect.signature(func)
    fparam, *params = signature.parameters.values()
    force_struct = fparam.name == 'prices'
    newsig = inspect.Signature(params)

    def wrapper(self, *args, **kwargs):
        expr = self._expr

        bound_args = newsig.bind(*args, **kwargs)
        args, kwargs = (), dict(bound_args.arguments)

        if force_struct and expr.meta.has_multiple_outputs():
            expr = pl.struct(expr)

        def batch_func(data):
            if force_struct:
                data = data.struct.unnest()

            output = func(data, *args, **kwargs)
            return wrap_polars(output, name=name)

        result = expr.map_batches(batch_func, return_dtype=output_type)

        return result

    return wrapper

def accessor_method(func):
    name = func.__name__
    name = name.removeprefix("calc_")
    sig = inspect.signature(func)
    fparam = list(sig.parameters.values())[0]

    def wrapper(self, *args, **kwargs):
        data = self._data
        if isinstance(data, pl.DataFrame) and fparam.name == "series":
            data = data['close']
        result = func(data, *args, **kwargs)
        return wrap_polars(result, name=name)
    
    return wrapper


@pl.api.register_dataframe_namespace(NAMESPACE)
class DataFrameCalc:
    def __init__(self, df: pl.DataFrame) -> None:
        self._data = df


@pl.api.register_series_namespace(NAMESPACE)
class SeriesCalc:
    def __init__(self, s: pl.Series) -> None:
        self._data = s


@pl.api.register_expr_namespace(NAMESPACE)
class ExpressionCalc:
    def __init__(self, expr: pl.Expr) -> None:
        self._expr = expr

    def next(self, p: int) -> pl.Expr:
        return (p ** (self._expr.log(p).ceil()).cast(pl.Int64)).cast(pl.Int64)



def setup():
    from . import core

    calc_methods = [m for m in dir(core) if m.startswith("calc_")]

    for cname in calc_methods:
        name = cname.removeprefix("calc_")
        func = getattr(core, cname) 
        sig = inspect.signature(func)
        fparam = list(sig.parameters.values())[0]

        wrapper = expression_method(func)
        setattr(ExpressionCalc, name, wrapper)

        wrapper = accessor_method(func)
        setattr(DataFrameCalc, name, wrapper)

        if fparam.name == "series":
            wrapper = accessor_method(func)
            setattr(SeriesCalc, name, wrapper)

            

setup()


