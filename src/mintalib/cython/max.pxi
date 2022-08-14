""" Maximum """


@export
def calc_max(series, long period=1):
    """ Maximum over a period """

    cdef double[:] xs = asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, res = NAN
    cdef long i = 0, j = 0, offset = period -1

    if period <= 0:
        return result

    for i in range(offset, size):
        res = xs[i - offset]
        for j in range(i - offset, i + 1):
            v = xs[j]
            if isnan(v):
                break
            if v > res:
                res = v
        else:
            output[i] = res

    result = wrap_result(result, series)

    return result

class MAX(Indicator):
    """ Maximum over a Period """

    def __init__(self, period : int = 1, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_max(series, self.period)
        return result
