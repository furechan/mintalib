# common imports to all pxi files

from libc cimport math
from libc.math cimport isnan

cdef double NAN = float('nan')

import sys
import numpy as np

from enum import IntEnum

from collections import namedtuple
from types import MappingProxyType



def check_size(*args):
    """check all series have the same size and return the size"""

    xs, *others = args

    cdef long size = xs.size
    for s in others:
        if s.size != size:
               raise ValueError("Different sizes!")
    return size



def column_accessor(data):
    """column accessor if applicable"""

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
    """get series from prices or series data"""

    columns = column_accessor(data)

    if columns is not None:
        if item is None:
            item = default_item
        return columns[item]

    if item is not None:
        tname = type(data).__name__
        raise ValueError(f"Cannot get series from {tname}")

    return data


def add_metadata(*, same_scale: bool = None, output_names: list | tuple = None):
    """update function with metadata"""

    if same_scale is not None:
        same_scale = bool(same_scale)

    if output_names is not None:
        output_names = tuple(output_names)

    metadata = dict(same_scale=same_scale, output_names=output_names)
    metadata = { k: v for k, v in metadata.items() if v is not None}

    def decorator(func):
        func.metadata = MappingProxyType(metadata)
        return func

    return decorator



def wrap_result(result, source, name: str = None):
    """wrap result to match source data type"""

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
            return pandas.Series(result, index=index, name=name)

    if pname == 'polars':
        polars = sys.modules['polars']

        if isinstance(result, dict):
            return polars.DataFrame(result).fill_nan(None)

        if isinstance(result, np.ndarray):
            return polars.Series(name=name, values=result).fill_nan(None)

    return result

