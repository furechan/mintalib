""" Streak """


def streak_up(series, *, wrap: bool = False):
    """ Consecutive streak of ups """

    cdef const double[:] xs = np.asarray(series, float)
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

    if wrap:
        result = wrap_result(result, series)

    return result




def streak_down(series, *, wrap: bool = False):
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

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(streak_up)
def STREAK_UP(series, *, item: str = None):
    series = get_series(series, item=item)
    result = streak_up(series)
    return wrap_result(result, series)


@wrap_function(streak_down)
def STREAK_DOWN(series, *, item: str = None):
    series = get_series(series, item=item)
    result = streak_down(series)
    return wrap_result(result, series)


