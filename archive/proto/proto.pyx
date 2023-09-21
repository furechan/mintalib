# cython: language_level=3, binding=True


from libc cimport math
from libc.math cimport isnan

cdef double NAN = float('nan')

import re
import numpy as np

from enum import IntEnum
from collections import namedtuple

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


def metadata(same_scale: bool=None):
    def modifier(func):
        if same_scale is not None:
            func.same_scale = same_scale
        return func
    return modifier


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
    """ wraps a result into dataframe/series similar to source """

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


@metadata(same_scale=True)
def calc_ema(series, long period, *, bint adjust = False, wrap: bool = False):
    """
    Exponential Moving Average

    Args:
        series (series) : data series, required
        period (int) : time period, required
        adjust (bool) : whether to adjust weights, default False
            when true update ratio increases gradually (see formula)

    Formula:
        EMA is calculated as a recursive formula
        The standard formula is ema += alpha * (value - ema)
            with alpha = 2.0 / (period + 1.0)
        The adjusted formula is ema = num/div
            where num = value + rho * num, div = 1.0 + rho * div
            with rho = 1.0 - alpha
    """

    if period <= 1:
        raise ValueError(f"Invalid period value {period}")

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double alpha = 2.0 / (period + 1.0)
    cdef double rho = (1.0 - alpha)
    cdef double value = NAN
    cdef double num = NAN, div=NAN
    cdef double ema = NAN

    cdef long i = 0, count = 0

    for i in range(size):
        value = xs[i]

        if not isnan(value):
            count += 1

            if isnan(ema):
                ema = value
                num = value
                div = 1.0
            elif adjust:
                num = value + rho * num
                div = 1.0 + rho * div
                ema = num / div
            else:
                ema += alpha * (value - ema)

        if count >= period:
            output[i] = ema

    if wrap:
        result = wrap_result(result, series)

    return result

