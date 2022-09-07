""" Standard Deviation """


@export
def calc_mad(series, long period):
    """ Mean Absolute Deviation """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, sx, mx

    cdef long i = 0, j = 0, count = 0
    cdef long maxlen = size - period + 1

    for i in range(maxlen):
        sx, count = 0, 0
        for j in range(period):
            x = xs[i + j]
            if isnan(x):
                break
            sx += x
            count += 1

        if count < period:
            continue

        mx = sx / count
        sx, count = 0, 0
        for j in range(period):
            x = xs[i + j]
            sx += fabs(x - mx)
            count += 1

        res = sx / count
        output[i + j] = res

    result = wrap_result(result, series)

    return result



class MAD(Indicator):
    """ Mean Absolue Deviation """

    def __init__(self, period : int, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_mad(series, self.period)
        return result
