""" Rolling Maximum """


def calc_max(series, long period, *, wrap: bool = False):
    """ Rolling Maximum """

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
            if not v <= res:
                res = v

        output[i + j] = res

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(calc_max)
def MAX(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_max(series, period=period)
    return wrap_result(result, series)

