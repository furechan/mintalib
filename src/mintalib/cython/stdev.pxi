""" Standard Deviation """


def calc_stdev(series, long period=20, *, wrap: bool = False):
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

    cdef double x, s, sx, sxx, vxx, std

    cdef long i = 0, j = 0

    cdef long maxlen = size - period + 1

    for i in range(maxlen):

        s = sx = sxx = 0.0

        for j in range(period):
            x = xs[i + j]

            if isnan(x):
                break

            s += 1.0
            sx += x
            sxx += x * x

        else:
            vxx = (sxx / s - sx * sx / s / s)
            std = math.sqrt(vxx) if vxx >= 0 else NAN
            output[i + j] = std

    if wrap:
        result = wrap_result(result, series)

    return result

