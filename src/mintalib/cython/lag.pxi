""" Lag function """


def calc_lag(series, long period, *, wrap: bool = False):
    """
    Lag Function

    Args:
        period (int) : time period, required
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN
    cdef long i = 0

    if period < 0 or period >= size:
        return result

    for i in range(period, size):
        v = xs[i - period]
        output[i] = v

    if wrap:
        result = wrap_result(result, series)

    return result


