""" Rate of Change """

def calc_roc(series, long period=1):
    """
    Rate of Change

    Returns rate of change as a percentage. For example, a 10% increase returns 10.0.

    Args:
        period (int): time period, default 1
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.empty(size, float)
    cdef double[:] output = result

    cdef double v = NAN, pv = NAN, roc = NAN
    cdef long i = 0

    if period <= 0:
        raise ValueError("period must be greater than zero")

    with nogil:
        for i in range(period if period < size else size):
            output[i] = NAN

        for i in range(period, size):
            v, pv = xs[i], xs[i - period]
            if pv != 0:
                roc = (v / pv - 1) * 100
                output[i] = roc
            else:
                output[i] = NAN

    return result
