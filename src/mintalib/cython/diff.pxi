""" Difference """




def calc_diff(series, long period=1, *, wrap: bool = False):
    """ Difference """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, pv = NAN, diff = NAN
    cdef long i = 0

    if period < 0 or period >= size:
        return result

    for i in range(period, size):
        v, pv = xs[i], xs[i - period]
        diff = v  - pv
        output[i] = diff

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(calc_diff)
def DIFF(series, period: int = 1, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_diff(series, period=period)
    return wrap_result(result, series)

