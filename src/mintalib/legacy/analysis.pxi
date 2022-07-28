#cython: language_level=3

import numpy as np

from libc.math cimport isnan, log, sqrt

cdef double NAN = float('nan')


__all__ = []

def export(func):
    __all__.append(func.__name__)
    return func

@export
def summary_from_positions(posdata, *, groupby=None, int ddof=1, context=()):

    cdef long long size = len(posdata)

    if groupby is not None:
        ngroup = posdata.groupby(groupby).ngroup()
    else:
        ngroup = np.full(size, 0)

    cdef double[:] _close = np.asarray(posdata.close, float)
    cdef double[:] _pos = np.asarray(posdata.pos, float)
    cdef long[:] _ngroup = np.asarray(ngroup, int)

    assert _pos.size == size, "pos has a different size"
    assert _close.size == size, "close has a different size"
    assert _ngroup.size == size, "ngroup has a different size"


    cdef double pos = NAN, ppos = NAN
    cdef double close = NAN, pclose = NAN
    cdef double ret = NAN

    cdef double span_long = 0.0, span_neutral = 0.0
    cdef double ret_long = 0.0, ret_neutral = 0.0
    cdef double ret2_long = 0.0, ret2_neutral = 0.0
    cdef double std_long = NAN, std_neutral = NAN

    cdef long count_long = 0, count_neutral = 0
    cdef long span = 0
    cdef long ng = 0
    cdef long i = 0

    for i in range(size):
        if _ngroup[i] != ng:
            ng = _ngroup[i]
            pclose = NAN
            ppos = NAN
            span = 0

        close = _close[i]
        pos = _pos[i]

        if isnan(close) or isnan(pos):
            continue

        if isnan(ppos):
            pclose = close
            ppos = pos
            span = 0
            continue

        span += 1

        if pos == ppos:
            continue

        ret = log(close/pclose) if pclose else 0.0
        if ppos > 0:
            count_long += 1
            span_long += span
            ret_long += ret
            ret2_long += ret * ret
        else:
            count_neutral += 1
            span_neutral += span
            ret_neutral += ret
            ret2_neutral += ret * ret

        pclose = close
        ppos = pos
        span = 0

    if count_long > ddof:
        span_long /= count_long
        ret_long /= count_long
        ret2_long = ret2_long / count_long - ret_long * ret_long
        std_long = ret2_long * count_long / (count_long - ddof)
        std_long = sqrt(std_long) if std_long >= 0 else NAN

    if count_neutral > ddof:
        span_neutral /= count_neutral
        ret_neutral /= count_neutral
        ret2_neutral = ret2_neutral / count_neutral - ret_neutral * ret_neutral
        std_neutral = ret2_long * count_neutral / (count_neutral - ddof)
        std_neutral = sqrt(std_neutral) if std_neutral >= 0 else NAN

    score = ret_long / std_long if std_long > 0 else NAN

    result = dict(context, score=score)

    result.update(ret_long=ret_long, std_long=std_long,
                  span_long=span_long, count_long=count_long)

    result.update(ret_neutral=ret_neutral, std_neutral=std_neutral,
                  span_neutral=span_neutral, count_neutral=count_neutral)

    return result

