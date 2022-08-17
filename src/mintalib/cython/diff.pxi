""" Difference """



@export
def calc_diff(series, long period=1, wrap: bool = True):
    """ Difference """

    cdef double[:] xs = asarray(series, float)
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


class DIFF(Indicator):
    """ Difference """

    def __init__(self, period: int = 1, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_diff(series, self.period, wrap=True)
        return result
