""" Rate of Change """

def calc_roc(series, long period=1, *, wrap: bool = False):
    """ Rate of Change """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, pv = NAN, roc = NAN
    cdef long i = 0

    if period >= size:
        return result

    for i in range(period, size):
        v, pv = xs[i], xs[i - period]
        roc = v / pv - 1 if pv != 0 else NAN
        output[i] = roc

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(calc_roc)
def ROC(series, period: int = 1, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_roc(series, period=period)
    return wrap_result(result, series)

