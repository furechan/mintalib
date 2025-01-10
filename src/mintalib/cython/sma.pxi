""" Simple Moving Average """

def calc_sma(series, long period, *, wrap: bool = False):
    """
    Simple Moving Average
    
    Args:
        period (int) : time period, required
    """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double divisor = period * (period + 1) / 2
    cdef double v = NAN, vsum = NAN
    cdef long i = 0, j = 0, count = 0

    cdef long maxlen = size - period + 1

    for i in range(maxlen):
        vsum, count = 0.0, 0

        for j in range(period):
            v = xs[i + j]

            if isnan(v):
                break

            vsum += v
            count += 1

        if count >= period:
            output[i + j] = vsum / count

    if wrap:
        result = wrap_result(result, series)

    return result

