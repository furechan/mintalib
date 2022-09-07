""" Rate of Change """


@export
def calc_roc(series, long period=1):
    """ Rate of Change """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef double[:] xs = np.asarray(series, float)
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

    result = wrap_result(result, series)

    return result


class ROC(Indicator):
    """ Rate of Change """

    def __init__(self, period : int = 1, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_roc(series, self.period)
        return result
