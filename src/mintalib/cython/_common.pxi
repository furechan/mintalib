from libc.math cimport fabs, isnan, log, exp, ceil, floor, sqrt

cdef double NAN = float('nan')

import numpy as np

from enum import IntEnum

from collections import namedtuple

from .model import Indicator

try:
    from pandas import Series as pdSeries
    from pandas import DataFrame as pdDataFrame

    Pandas = (pdSeries, pdDataFrame)

except ModuleNotFoundError:
    pdSeries = ()
    pdDataFrame = ()
    Pandas = ()


try:
    from polars import Series as plSeries
    from polars import DataFrame as plDataFrame

    Polars = (plSeries, plDataFrame)

except ModuleNotFoundError:
    plSeries = ()
    plDataFrame = ()
    Polars = ()


def export(target):
    name = getattr(target, "__name__", str(target))
    globals().setdefault('__all__', []).append(name)
    return target


def asarray(data, dtype=float):
    if hasattr(data, "to_numpy"):
        result = data.to_numpy().astype(dtype)
    else:
        result = np.asarray(data, dtype)

    return result


def check_size(xs, *others):
    cdef long size = xs.size
    for s in others:
        if s.size != size:
               raise ValueError("Different sizes!")
    return size


def wrap_result(result, source):
    if isinstance(result, tuple):
        result = result._asdict()

    if isinstance(source, Pandas):
        if isinstance(result, dict):
            return pdDataFrame(result, index=source.index)

        if isinstance(result, np.ndarray):
            return pdSeries(result, index=source.index)

    if isinstance(source, Polars):
        if isinstance(result, dict):
            return plDataFrame(result)

        if isinstance(result, np.ndarray):
            return plSeries(result)

    return result

