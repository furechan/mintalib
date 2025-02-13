""" Standard Deviation """


def calc_stdev(series, long period=20, *, bint wrap=False):
    """
    Standard Deviation
    
    Args:
        period (int) : time period, default 20
    """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x = NAN, vxx = NAN, std = NAN

    cdef double sx = 0.0, sxx = 0.0

    cdef long i = 0, j = 0, count = 0

    for i in range(size):
        x = xs[i]

        if x == x:
            count += 1
            sx += x
            sxx += x * x
        else:
            count = 0
            sx = sxx = 0.0

        while count > period and j < i:
            x, j = xs[j], j + 1
            if x == x:
                count -= 1
                sx -= x
                sxx -= x * x

        if count == period:
            vxx = (sxx / count - sx * sx / count / count)
            std = math.sqrt(vxx) if vxx >= 0 else NAN
            output[i] = std

    if wrap:
        result = wrap_result(result, series)

    return result

