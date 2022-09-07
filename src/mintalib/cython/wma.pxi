""" Weighted Moving Average """


@export
def calc_wma(series, long period, wrap: bool = True):
    """ Weighted Moving Average """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef double[:] xs = np.asarray(series, float)
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


class WMA(Indicator):
    """ Weighted Moving Average """

    same_scale = True

    def __init__(self, period: int, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_wma(series, self.period, wrap=True)
        return result
