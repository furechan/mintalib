""" Simple Moving Average """


@export
def calc_sma(series, int period=20):
    """
    Simple Moving Average

    Args:
        series : data series. required
        period (int) : time period. default 20
    """

    cdef double[:] xs = asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, rsum = 0
    cdef long i = 0, j = 0, count = 0

    for i in range(size):
        v = xs[i]

        if not isnan(v):
            rsum += v
            count += 1

        while count > period and j < i:
            v, j = xs[j], j+1
            if not isnan(v):
                rsum -= v
                count -= 1

        if count >= period:
            output[i] = rsum / count

    result = wrap_result(result, series)

    return result


@export
class SMA(Indicator):
    """
    Simple Moving Average

    Args:
        period (int) : time period. default 20
    """

    same_scale = True

    def __init__(self, period=50, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_sma(series, self.period)
        return result
