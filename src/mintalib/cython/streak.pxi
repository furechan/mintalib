""" Streak """


@export
def calc_streak(series):
    """ streak """

    cdef double[:] xs = asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double value = NAN, prev = NAN, diff=NAN
    cdef double streak = NAN

    cdef long i = 0

    for i in range(size):
        value = xs[i]

        if not isnan(value):
            diff, prev = value - prev, value

            if isnan(diff):
                pass

            if diff > 0:
                diff = 1
            elif diff < 0:
                diff = -1
            else:
                diff = 0

            if streak * diff >= 0:
                streak += diff
            else:
                streak = diff

        output[i] = streak

    result = wrap_result(result, series)

    return result

