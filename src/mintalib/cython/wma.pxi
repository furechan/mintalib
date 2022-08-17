""" Weighted Moving Average """


@export
def calc_wma(series, long period, wrap: bool = True):
    """ Weighted Moving Average """

    cdef double[:] xs = asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double divisor = period * (period + 1) / 2
    cdef double v=NAN, sum=NAN
    cdef long i=0, j=0

    cdef long maxlen = size - period + 1

    if maxlen <= 0:
        return result

    for i in range(maxlen):
        sum = 0.0

        for j in range(period):
            v = xs[i + j]

            if isnan(v):
                break

            sum += v * (j+1)
        else:
            output[i + j] = sum / divisor

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
