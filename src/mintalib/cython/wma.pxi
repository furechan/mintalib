""" Weighted Moving Average """

def calc_wma(series, long period, *, wrap: bool = False):
    """
    Weighted Moving Average
        
    Args:
        period (int) : time period, required
    """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double divisor = period * (period + 1) / 2
    cdef double v = NAN, wsum = NAN
    cdef long i = 0, j = 0

    cdef long maxlen = size - period + 1

    for i in range(maxlen):
        wsum = 0.0

        for j in range(period):
            v = xs[i + j]

            if isnan(v):
                break

            wsum += v * (j+1)
        else:
            output[i + j] = wsum / divisor

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(calc_wma, same_scale=True)
def WMA(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_wma(series, period=period)
    return wrap_result(result, series)

