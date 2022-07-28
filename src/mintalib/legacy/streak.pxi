#cython: language_level=3

import numpy as np

from libc.math cimport isnan

cdef double NAN = float('nan')

def export(target):
    name = getattr(target, "__name__", str(target))
    globals().setdefault('__all__', []).append(name)
    return target



@export
def streak_up(data):
    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double value = NAN, prev = NAN
    cdef double streak = NAN

    cdef long i = 0

    for i in range(size):
        value = xs[i]

        if not isnan(value):
            if value > prev:
                streak += 1
            else:
                streak = 0
            prev = value

        output[i] = streak

    return result

@export
def streak_down(data):
    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double value = NAN, prev = NAN
    cdef double streak = NAN

    cdef long i = 0

    for i in range(size):
        value = xs[i]

        if not isnan(value):
            if value < prev:
                streak += 1
            else:
                streak = 0
            prev = value

        output[i] = streak

    return result

