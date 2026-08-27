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

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, pv = NAN, rocp = NAN
    cdef long i = 0

    if period < 0:
        raise ValueError(f"Invalid period value {period}")

    with nogil:
        for i in range(period, size):
            v, pv = xs[i], xs[i - period]
            if v > 0 and pv > 0:
                rocp = v / pv - 1
                output[i] = rocp

    return result
