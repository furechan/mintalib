""" Rolling Mean Absolute Deviation """


def calc_mad(series, long period=14):
    """Rolling Mean Absolute Deviation"""

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, mean, mad
    cdef double sx = 0.0
    cdef long i = 0, k = 0, count = 0

    for i in range(size):
        x = xs[i]

        if x == x:
            count += 1
            sx += x
        else:
            count = 0
            sx = 0.0

        if count > period:
            sx -= xs[i - period]
            count -= 1

        if count == period:
            mean = sx / period
            mad = 0.0
            for k in range(i - period + 1, i + 1):
                mad += math.fabs(xs[k] - mean)
            output[i] = mad / period

    return result
