# common imports to all pxi files

from libc.math cimport fabs, isnan, log, exp, ceil, floor, sqrt

cdef double NAN = float('nan')


import re
import numpy as np

from enum import IntEnum

from collections import namedtuple

from .model import Indicator

try:
    from pandas import Series as pdSeries
    from pandas import DataFrame as pdDataFrame

    # collective type of Pandas data objects
    Pandas = (pdSeries, pdDataFrame)

except ModuleNotFoundError:
    pdSeries = ()
    pdDataFrame = ()
    Pandas = ()


try:
    from polars import Series as plSeries
    from polars import DataFrame as plDataFrame

    # collective type of Polars data objects
    Polars = (plSeries, plDataFrame)

except ModuleNotFoundError:
    plSeries = ()
    plDataFrame = ()
    Polars = ()


def export(target):
    """ add target name to ___all__ """
    name = getattr(target, "__name__", str(target))
    globals().setdefault('__all__', []).append(name)
    return target


def check_size(xs, *others):
    """ check all series have the same size and return the size """
    cdef long size = xs.size
    for s in others:
        if s.size != size:
               raise ValueError("Different sizes!")
    return size


def wrap_indicator(source):
    """ updates indicator class with function documentation """
    doc = source.__doc__

    if doc is not None:
        ignore = "(?xm) \n \s+ (series|prices|wrap) \s+ [^\n:]* : [^\n]+ \n"
        doc = re.sub(ignore, '', doc)

    def decorator(func):
        func.__doc__ = doc
        return func

    return decorator


def wrap_result(result, source):
    """ createa a result dataframe/series from source """

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

