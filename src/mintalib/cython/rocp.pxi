""" Rate of Change Percentage """

def calc_rocp(series, long period=1):
    """
    Rate of Change Percentage

    Returns rate of change as a fraction. For example, a 10% increase returns 0.1.

    Args:
        period (int): time period, default 1
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.empty(size, float)
    cdef double[:] output = result

    cdef double v = NAN, pv = NAN, rocp = NAN
    cdef long i = 0

    if period <= 0:
        raise ValueError("period must be greater than zero")

    with nogil:
        for i in range(period if period < size else size):
            output[i] = NAN

        for i in range(period, size):
            v, pv = xs[i], xs[i - period]
            if pv != 0:
                rocp = v / pv - 1
                output[i] = rocp
            else:
                output[i] = NAN

    return result
