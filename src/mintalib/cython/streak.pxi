""" Streak """


@export
def streak_up(series):
    """ Consecutive streak of ups """

    cdef double[:] xs = np.asarray(series, float)
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

            if diff > 0:
                streak += 1
            elif diff < 0:
                streak = 0

        output[i] = streak

    result = wrap_result(result, series)

    return result




@export
def streak_down(series):
    """ Consecutive streak of ups """

    cdef double[:] xs = np.asarray(series, float)
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

            if diff < 0:
                streak += 1
            elif diff > 0:
                streak = 0

        output[i] = streak

    result = wrap_result(result, series)

    return result


