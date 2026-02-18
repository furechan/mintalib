""" Lag function """


@add_metadata(same_scale=True)
def calc_lag(series, long period):
    """
    Lag Function

    Args:
        period (int) : time period, required
    """

    if period < 0:
        raise ValueError("Period cannot be negative")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = np.nan
    cdef long i = 0

    for i in range(period, size):
        v = xs[i - period]
        output[i] = v

    return result


