""" Difference """


def calc_diff(series, long period=1):
    """Difference

    Difference between current value and the one offset by period

    Args:
        period (int) : time period, default 1
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, pv = NAN, diff = NAN

    cdef long i = 0

    if period < 0 or period >= size:
        raise ValueError(f"Period {period} out of range!")

    for i in range(period, size):
        v, pv = xs[i], xs[i - period]
        diff = v  - pv
        output[i] = diff

    return result

