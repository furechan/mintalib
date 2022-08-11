from libc.math cimport fabs, isnan, log, exp, ceil, floor, sqrt

cdef double NAN = float('nan')

import numpy as np

from enum import Enum, IntEnum

from .model import Indicator

try:
    from pandas import Index, Series, DataFrame
except ModuleNotFoundError:
    Index = Series = DataFrame = ()


def export(target):
    name = getattr(target, "__name__", str(target))
    globals().setdefault('__all__', []).append(name)
    return target


def make_series(result, source, name=None):
    if isinstance(source, Index):
        index = source
    elif isinstance(source, Series):
        index = source.index
    elif isinstance(source, DataFrame):
        index = source.index
    else:
        return result

    return Series(result, index=index, name=name)


def make_dataframe(result, source, columns=None):
    if isinstance(source, Index):
        index = source
    elif isinstance(source, Series):
        index = source.index
    elif isinstance(source, DataFrame):
        index = source.index
    else:
        return result

    if columns is not None and isinstance(result, tuple):
        result = dict(zip(columns, result))

    return DataFrame(result, index=index, columns=columns)


def compare_sizes(*series):
    sizes = [xs.size for xs in series]
    return len(set(sizes)) == 1


def extract_items(prices, items, *, bint check_size=True):
    count = len(items)

    if isinstance(prices, tuple):
        if len(tuple) != count:
            raise ValueError(f"Expected {count} items")
        result = prices

    elif hasattr(prices, 'columns') and hasattr(prices, '__getitem__'):
        result = tuple(prices[i] for i in items)

    else:
        raise ValueError(f"Cannot extract {items}")

    if check_size:
        sizes = [xs.size for xs in result]
        if len(set(sizes)) != 1:
            raise ValueError("Inputs have different sizes!")

    return result
