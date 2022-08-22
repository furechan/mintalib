""" Standard Deviation """


@export
def calc_mad(series, long period):
    """ Mean Absolute Deviation """

    cdef double[:] xs = asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, s, sx, mx

    cdef long i, j

    cdef bint skip

    if period > size:
        return result

    for j in range(period-1, size):
        skip = False

        s = sx = 0.0
        i = j - period + 1
        while i <= j:
            x = xs[i]
            if isnan(x):
                skip = True
                break
            sx += x
            s += 1.0
            i += 1

        if skip:
            continue

        mx = sx / s

        s = sx = 0.0
        i = j - period + 1
        while i <= j:
            x = xs[i]
            sx += fabs(x - mx)
            s += 1.0
            i += 1

        res = sx / s
        output[j] = res

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
