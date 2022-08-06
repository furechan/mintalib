""" Rate of Change """



@export
def calc_roc(series, int period=1):
    """ Rate of Change """

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, pv = NAN, roc = NAN
    cdef long i = 0

    if period <= 0:
        return result

    for i in range(period, size):
        v, pv = xs[i], xs[i - period]
        roc = v / pv - 1 if pv > 0 else NAN
        output[i] = roc

    if isinstance(series, Series):
        result = make_series(result, series)

    return result


class ROC(Indicator):
    """ Rate of Change """

    def __init__(self, period=1, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_roc(series, self.period)
        return result
