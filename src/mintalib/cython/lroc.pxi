""" Logarithmic Rate of Change """

def calc_lroc(series, long period=1):
    """
    Logarithmic Rate of Change

    Equivalent to the difference of log values

    Args:
        period (int): time period, default 1
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double v = NAN, pv = NAN, roc = NAN
    cdef long i = 0

    if period <= 0:
        raise ValueError("period must be greater than zero")

    with nogil:
        for i in range(period, size):
            v, pv = xs[i], xs[i - period]
            if v > 0 and pv > 0:
                roc = math.log(v / pv)
                output[i] = roc

    return result
