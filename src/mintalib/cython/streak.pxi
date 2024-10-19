""" Streak """


def calc_streak(series, *, wrap: bool = False):
    """
    Consecutive streak of ups or downs
    
    Length of streak of values all up or down, times +1 or -1 whether ups or downs.
    """

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
                streak = streak + 1 if streak>0 else 1.0 
            elif diff < 0:
                streak = streak - 1 if streak<0 else -1.0 

        output[i] = streak

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(calc_streak)
def STREAK(series, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_streak(series)
    return wrap_result(result, series)


