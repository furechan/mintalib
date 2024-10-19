""" Relative Strencgth Index """


def calc_rsi(series, long period=14, *, wrap: bool = False):
    """
    Relative Strength Index
    
    Args:
        period (int) : time period, default 14
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double alpha = 1.0 / period
    cdef double v = NAN, pv = NAN, dv = NAN
    cdef double up = NAN, down = NAN, rsi = NAN

    cdef double ups=0.0, downs=0.0
    cdef long i = 0, count = 0

    for i in range(size):
        v = xs[i]

        if isnan(v):
            pass

        elif isnan(pv):
            pv = v

        else:
            count += 1
            dv, pv = v - pv, v
            up, down= (dv, 0.0) if dv >= 0.0 else (0.0, -dv)

            if count <= period:
                ups += up * alpha
                downs += down * alpha
            else:
                ups += (up - ups) * alpha
                downs += (down - downs) * alpha

            if downs > 0 and count >= period:
                rsi = 100.0 - (100.0 / (1.0 + ups / downs))

        if not isnan(rsi):
            output[i] = rsi

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(calc_rsi)
def RSI(series, period: int = 14, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_rsi(series, period=period)
    return wrap_result(result, series)

