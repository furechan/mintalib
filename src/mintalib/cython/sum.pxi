""" Sum """

@export
def calc_sum(series, long period):
    """ Rolling Sum """

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
            output[i] = rsum

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
