""" Sum """



@export
def calc_sum(series, long period, wrap: bool = True):
    """ Rolling Sum """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double divisor = period * (period + 1) / 2
    cdef double v = NAN, vsum = NAN
    cdef long i = 0, j = 0, count = 0

    cdef long maxlen = size - period + 1

    for i in range(maxlen):
        vsum = 0.0
        count = 0

        for j in range(period):
            v = xs[i + j]

            if isnan(v):
                break

            vsum += v
            count += 1

        if count >= period:
            output[i + j] = vsum

    if wrap:
        result = wrap_result(result, series)

    return result




class SUM(Indicator):
    """ Rolling Sum """

    same_scale = True

    def __init__(self, period: int, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_sum(series, self.period)
        return result
