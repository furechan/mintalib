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


def _is_prices(data):
    """Return whether data is a supported prices container."""

    if isinstance(data, np.ndarray):
        return data.dtype.names is not None

    if hasattr(data, "columns"):
        return True

    return hasattr(data, "dtype") and data.dtype.__class__.__name__ == "Struct"



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

    asdict = getattr(result, '_asdict', None)
    if asdict is not None:
        result = asdict()

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


def _get_inputs(calc_func) -> tuple[str, ...]:
    metadata = getattr(calc_func, "metadata", {})
    declared_inputs = metadata.get("inputs")

    if not declared_inputs:
        raise ValueError(f"Missing inputs metadata for {calc_func.__name__!r}")

    return tuple(declared_inputs)


def _get_source(columns):
    return columns["close"] if "close" in columns else next(iter(columns.values()))


def _update_wrapper(wrapper, func, calc_func, signature):
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    wrapper.__module__ = func.__module__
    wrapper.__doc__ = calc_func.__doc__
    setattr(wrapper, "metadata", getattr(calc_func, "metadata", {}))
    setattr(wrapper, "__signature__", signature)
    return wrapper


def wrap_series_function(calc_func) -> Callable[[Callable[P, Any]], Callable[P, Any]]:
    first_param = next(iter(inspect.signature(calc_func).parameters))
    if first_param != "series":
        raise ValueError(f"Expected a series kernel, got {calc_func.__name__!r}")

    def decorator(func):
        signature = inspect.signature(func)

        def wrapper(*args, **kwargs):
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            arguments = dict(bound.arguments)
            source = _get_series(arguments.pop("series"))
            result = calc_func(source, **arguments)
            return _wrap_result(result, source)

        return _update_wrapper(wrapper, func, calc_func, signature)

    return decorator


def wrap_prices_function(calc_func) -> Callable[[Callable[P, Any]], Callable[P, Any]]:
    first_param = next(iter(inspect.signature(calc_func).parameters))
    if first_param != "prices":
        raise ValueError(f"Expected a prices kernel, got {calc_func.__name__!r}")

    inputs = _get_inputs(calc_func)

    def decorator(func):
        signature = inspect.signature(func)

        def wrapper(*args, **kwargs):
            if args:
                srcdata, *rest = args
                if _is_prices(srcdata):
                    if rest:
                        raise TypeError("too many positional arguments")
                    if "prices" in kwargs:
                        raise TypeError("multiple values for argument 'prices'")
                    data = _get_prices(srcdata)
                    result = calc_func(data, **kwargs)
                    return _wrap_result(result, srcdata)

            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            arguments = dict(bound.arguments)
            columns = {
                name: _get_series(arguments.pop(name))
                for name in inputs
            }
            result = calc_func(columns, **arguments)
            return _wrap_result(result, _get_source(columns))

        return _update_wrapper(wrapper, func, calc_func, signature)

    return decorator


def wrap_columns_function(calc_func) -> Callable[[Callable[P, Any]], Callable[P, Any]]:
    inputs = _get_inputs(calc_func)
    params = tuple(inspect.signature(calc_func).parameters)
    if params[: len(inputs)] != inputs:
        raise ValueError(f"Column inputs do not match parameters for {calc_func.__name__!r}")

    def decorator(func):
        signature = inspect.signature(func)

        def wrapper(*args, **kwargs):
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            arguments = dict(bound.arguments)

            columns = {
                name: _get_series(arguments.pop(name))
                for name in inputs
            }
            result = calc_func(*columns.values(), **arguments)
            return _wrap_result(result, _get_source(columns))

        return _update_wrapper(wrapper, func, calc_func, signature)

    return decorator
