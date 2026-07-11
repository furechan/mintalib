"""Function Model"""

import sys
import inspect

import numpy as np

from typing import ParamSpec, Callable, Any

P = ParamSpec("P")


def _get_prices(data):
    """Get prices data frame, raises on error
    
    Accepts a pandas or polars data frame, or a structured numpy ndarray.
    """

    if isinstance(data, np.ndarray):
        if data.dtype.names is not None:
            return data
        else:
            raise TypeError(f"Ndarray must have named fields to be used as data frame, got {data.dtype}!")
   
    elif hasattr(data, 'columns'):
        return data

    elif hasattr(data, 'dtype') and data.dtype.__class__.__name__ == 'Struct':
        return data.struct

    raise TypeError(f"Expected a prices data frame, got {type(data).__name__}!")



def _get_series(data):
    """Get series, raises on error

    Accepts a 1-dimensional pandas or polars series, or a 1-dimensional numpy ndarray.
    """

    shape = getattr(data, "shape", ())

    if not shape:
        raise TypeError(f"Expected a series, got {type(data).__name__}!")

    if len(shape) != 1:
        raise TypeError(f"Series is wrong shape {shape}!")
    
    return data



def _wrap_result(result, source, name: str | None = None):
    pname = getattr(source, '__module__', '').partition('.')[0]

    if isinstance(result, tuple) and hasattr(result, '_asdict'):
        result = result._asdict()

    if pname == 'pandas':
        pandas = sys.modules['pandas']
        index = getattr(source, 'index', None)

        if isinstance(result, dict):
            return pandas.DataFrame(result, index=index)

        if isinstance(result, np.ndarray):
            return pandas.Series(result, index=index, name=name)

    if pname == 'polars':
        polars = sys.modules['polars']

        if isinstance(result, dict):
            return polars.DataFrame(result).fill_nan(None)

        if isinstance(result, np.ndarray):
            return polars.Series(name=name, values=result).fill_nan(None)

    return result


def wrap_function(calc_func) -> Callable[[Callable[P, Any]], Callable[P, Any]]:
    """Decorator to wrap indicators"""

    sig = inspect.signature(calc_func)
    first_param = next(iter(sig.parameters))

    def decorator(func):
        sig = inspect.signature(func)

        def wrapper(srcdata, *args, **kwargs):
            if first_param == 'series':
                data = _get_series(srcdata)
            else:
                data = _get_prices(srcdata)

            result = calc_func(data, *args, **kwargs)
            return _wrap_result(result, srcdata)

        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__module__ = func.__module__
        wrapper.__doc__ = calc_func.__doc__
        wrapper.__signature__ = sig  # ty: ignore[unresolved-attribute]

        return wrapper
    return decorator

