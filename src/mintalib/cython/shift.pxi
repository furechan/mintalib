""" Shift function """

@add_metadata(same_scale=True)
def calc_shift(series, long period):
    """
    Shift Function

    Args:
        period (int): time period, required
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef long i = 0

    if period <= 0:
        raise ValueError("period must be greater than zero")

    with nogil:
        for i in range(period, size):
            output[i] = xs[i - period]

    return result

