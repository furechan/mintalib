""" Logarithmic Rate of Change """

def calc_lroc(series, long period=1, *, bint wrap=False):
    """
    Logarithmic Rate of Change

    Equivalent to the difference of log values

    Args:
        period (int) : time period, default 1
        when negative the calculation is shifted back
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, pv = NAN, roc = NAN
    cdef long i = 0, shift = 0

    if period < 0:
        period = abs(period)
        shift = -period

    for i in range(period, size):
        v, pv = xs[i], xs[i - period]
        if v > 0 and pv > 0:
            roc = math.log(v / pv)
            output[i + shift] = roc

    if wrap:
        result = wrap_result(result, series)

    return result

