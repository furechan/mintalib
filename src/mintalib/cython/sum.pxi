""" Rolling Sum """

@with_metadata(same_scale=True)
def calc_sum(series, long period, *, bint wrap=False):
    """
    Rolling sum
    
    Args:
        period (int) : time period, required
    """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, rsum = 0.0
    cdef long i = 0, j = 0, count = 0

    for i in range(size):
        v = xs[i]

        if v == v:
            rsum += v
            count += 1
        else:
            rsum = 0.0
            count = 0

        while count > period and j < i:
            v, j = xs[j], j + 1
            if v == v:
                rsum -= v
                count -= 1

        if count == period:
            output[i] = rsum

    if wrap:
        result = wrap_result(result, series)

    return result

