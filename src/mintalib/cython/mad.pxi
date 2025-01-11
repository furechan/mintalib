""" Standard Deviation """

def calc_mad(series, long period=20, *, bint wrap=False):
    """
    Mean Absolute Deviation
    
    Args:
        period (int) : time period, default 20
    """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, sx, mx

    cdef long i = 0, j = 0, count = 0
    cdef long maxlen = size - period + 1

    for i in range(maxlen):
        sx, count = 0, 0
        for j in range(period):
            x = xs[i + j]
            if isnan(x):
                break
            sx += x
            count += 1

        if count < period:
            continue

        mx = sx / count
        sx, count = 0, 0
        for j in range(period):
            x = xs[i + j]
            sx += math.fabs(x - mx)
            count += 1

        res = sx / count
        output[i + j] = res

    if wrap:
        result = wrap_result(result, series)

    return result


