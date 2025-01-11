""" Rolling Minimum """

@with_metadata(same_scale=True)
def calc_min(series, long period, *, bint wrap=False):
    """
    Rolling Minimum
    
    Args:
        period (int) : time period, required
    """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, res = NAN

    cdef long maxlen = size - period + 1
    cdef long i = 0, j = 0

    for i in range(maxlen):
        res = NAN

        for j in range(period):
            v = xs[i + j]
            if isnan(v):
                continue
            if not v >= res:
                res = v

        output[i + j] = res

    if wrap:
        result = wrap_result(result, series)

    return result


