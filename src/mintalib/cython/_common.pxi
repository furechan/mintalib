# common imports to all pxi files

from libc cimport math
from libc.math cimport isnan

cdef double NAN = float('nan')

import sys

import numpy as np

from enum import IntEnum

from collections import namedtuple


def check_size(xs, *others):
    """ check all series have the same size and return the size """

    cdef long size = xs.size
    for s in others:
        if s.size != size:
               raise ValueError("Different sizes!")
    return size



def column_accessor(data):
    """ column accessor if applicable """

    # Standard Dictionary
    if isinstance(data, dict):
        return data

    # Numpy record array 
    if isinstance(data, np.ndarray):
        if data.dtype.names is not None:
            return data
        return None

    # Regular dataframe (pandas & polars)
    if hasattr(data, 'columns'):
        return data

    # Struct Series (polars)
    if hasattr(data, 'dtype') and data.dtype.__class__.__name__ == 'Struct':
        return data.struct

    return  None



def get_series(data, item: str = None, *, default_item: str = 'close'):
    """ get series from prices or series data """

    columns = column_accessor(data)

    if columns is not None:
        if item is None:
            item = default_item
        return columns[item]

    if item is not None:
        tname = type(data).__name__
        raise ValueError(f"Cannot get series from {tname}")

    return data


def get_array(data, item: str = None, *, default_item: str = 'close', dtype=None):
    """ get array from prices or series data """

    series = get_series(data, item, default_item=default_item)

    return np.asarray(series, dtype=dtype)


def get_arrays(data, items: str = None, *, dtype=None):
    """ get arrays from prices data """

    series = [get_series(data, item) for item in items]
    arrays = tuple(np.asarray(s, dtype=dtype) for s in series)

    return arrays



def wrap_function(source, same_scale: bool = None):
    """ update function with documentation from source """

    doc = str(source.__doc__) if source else None

    metadata = dict(same_scale=same_scale)
    metadata = { k: v for k, v in metadata.items() if v is not None}

    if doc and metadata:
        doc = doc.rstrip()
        doc += "\n\n    Attributes:\n"
        for k, v in metadata.items():
            doc += f"        {k} = {v!r}\n"

    def decorator(func):
        if doc and func.__doc__ is None:
            func.__doc__ = doc
        for name, value in metadata.items():
            setattr(func, name, value)
        return func

    return decorator


def wrap_indicator(source):
    """ update indicator with documentation from source """

    doc = source.__doc__ if source else None

    def decorator(func):
        if doc and func.__doc__ is None:
            func.__doc__ = doc
        return func

    return decorator


def wrap_result(result, source):
    """ wrap result to match source data form (pandas, polars) """

    pname = getattr(source, '__module__', '').partition('.')[0]

    # convert namedtuple to dict
    if isinstance(result, tuple) and hasattr(result, '_asdict'):
        result = result._asdict()

    if pname == 'pandas':
        pandas = sys.modules['pandas']
        index = getattr(source, 'index', None)

        if isinstance(result, dict):
            return pandas.DataFrame(result, index=index)

        if isinstance(result, np.ndarray):
            return pandas.Series(result, index=index)

    if pname == 'polars':
        polars = sys.modules['polars']

        if isinstance(result, dict):
            return polars.DataFrame(result)

        if isinstance(result, np.ndarray):
            return polars.Series(result)

    return result

