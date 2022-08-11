""" Difference """



@export
def calc_diff(series, int period=1):
    """ Difference """

    cdef double[:] xs = np.asarray(series, float)
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

    if isinstance(series, Series):
        result = make_series(result, series)

    return result


class DIFF(Indicator):
    """ Difference """

    def __init__(self, period=1, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_diff(series, self.period)
        return result
