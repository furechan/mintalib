# cython: language_level=3, binding=True

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
    if isinstance(source, Series):
        index = source.index
    elif isinstance(source, Index):
        index = source
    else:
        return result

    return Series(result, index=index, name=name)


def make_dataframe(result, source, columns=None):
    if isinstance(source, Series):
        index = source.index
    elif isinstance(source, Index):
        index = source
    else:
        return result

    if columns is not None and isinstance(result, tuple):
        result = dict(zip(columns, result))

    return DataFrame(result, index=index, columns=columns)


include "cython/_all_core.pxi"

