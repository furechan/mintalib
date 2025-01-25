""" Lag function """


@with_metadata(same_scale=True)
def calc_lag(series, long period, *, bint wrap=False):
    """
    Lag Function

    Args:
        period (int) : time period, required
    """

    if period < 0:
        raise ValueError("Period cannot be negative")

    cdef const double[:] xs = np.asarray(series, np.float64)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = np.nan
    cdef long i = 0

    for i in range(period, size):
        v = xs[i - period]
        output[i] = v

    if wrap:
        result = wrap_result(result, series)

    return result


