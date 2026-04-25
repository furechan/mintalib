""" Rolling Maximum """

@add_metadata(same_scale=True)
def calc_max(series, long period):
    """ Rolling Maximum """

    if period <= 0:
        raise ValueError("Period must be positive")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, cur_max = NAN
    cdef long i = 0, j = 0, max_idx = -1

    for i in range(period - 1, size):
        v = xs[i]

        if max_idx >= i - period + 1:
            if not v <= cur_max:
                cur_max = v
                max_idx = i
        else:
            cur_max = NAN
            max_idx = -1
            for j in range(i - period + 1, i + 1):
                v = xs[j]
                if not isnan(v) and not v <= cur_max:
                    cur_max = v
                    max_idx = j

        output[i] = cur_max

    return result
