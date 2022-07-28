#cython: language_level=3

import numpy as np

# cimport cython
# cimport numpy as cnp
# from .finance import calc_rma
# cdef extern from "Python.h":
#     int PyCFunction_Check(object obj)
# __all__ = [k for k, v in globals().items() if getattr(v, '__module__', None) == __name__ ]


from libc.math cimport isnan, sqrt

cdef double NAN = float('nan')


__all__ = []

def export(func):
    __all__.append(func.__name__)
    return func


@export
def np_signal(buy, sell):
    """ returns of 1 or 0 according to buy/sell signals """

    cdef long[:] xs1 = np.where(buy, 1, 0)
    cdef long[:] xs2 = np.where(sell, 1, 0)
    cdef long size = xs1.size

    if xs1.size != xs2.size:
        raise ValueError("array sizes do no match!")

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double pos=NAN
    cdef long v1=0, v2=0
    cdef long i=0

    for i in range(0, size):
        v1, v2 = xs1[i], xs2[i]
        if v2:
            pos = 0.0
        elif pos == 0 and v1:
            pos = 1.0
        output[i] = pos

    return result

@export
def calc_volatility(data, double n, bint wrap=True):
    """ rolling volatility of returns (not annualized) """

    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double alpha = 2.0 / (n + 1.0)
    cdef double value=NAN, prev=NAN
    cdef double x=0.0, sx=0.0, sxx=0.0, vxx=0.0, vola=0.0
    cdef long i=0, skip=int(n)

    for i in range(size):
        if value >= 0:
            prev = value
        value = xs[i]
        if isnan(prev) or isnan(value) or value <= 0:
            continue
        x = (value / prev - 1.0)
        sx += alpha * (x - sx)
        sxx += alpha * (x * x - sxx)
        vxx = sxx - sx * sx
        vola = sqrt(vxx) if vxx > 0 else 0.0
        if skip > 0:
            skip -= 1
        else:
            output[i] = vola

    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result
