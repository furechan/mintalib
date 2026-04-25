""" Rolling Minimum """

@add_metadata(same_scale=True)
def calc_min(series, long period):
    """
    Rolling Minimum

    Args:
        period (int) : time period, required
    """

    if period <= 0:
        raise ValueError("Period must be positive")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, cur_min = NAN
    cdef long i = 0, j = 0, min_idx = -1

    for i in range(period - 1, size):
        v = xs[i]

        if min_idx >= i - period + 1:
            if not v >= cur_min:
                cur_min = v
                min_idx = i
        else:
            cur_min = NAN
            min_idx = -1
            for j in range(i - period + 1, i + 1):
                v = xs[j]
                if not isnan(v) and not v >= cur_min:
                    cur_min = v
                    min_idx = j

        output[i] = cur_min

    return result
