""" Rolling Maximum """


@export
def calc_max(series, long period):
    """ Rolling Maximum """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, res = NAN

    cdef long maxlen = size - period + 1
    cdef long i = 0, j = 0

    for i in range(maxlen):
        res = NAN

        for j in range(period):
            v = xs[i + j]
            if isnan(v):
                continue
            if not v <= res:
                res = v

        output[i + j] = res

    result = wrap_result(result, series)

    return result


class MAX(Indicator):
    """ Rolling Maximum """

    def __init__(self, period : int, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_max(series, self.period)
        return result
