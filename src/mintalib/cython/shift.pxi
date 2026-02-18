""" Shift function """


@add_metadata(same_scale=True)
def calc_shift(series, long period):
    """
    Shift Function

    Args:
        period (int) : time period, required
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef long i=0, start = period, stop = size

    if period < 0:
        start, stop = 0, size + period

    for i in range(start, stop):
        output[i] = xs[i - period]

    return result


