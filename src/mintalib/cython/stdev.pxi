""" Standard Deviation """


@export
def calc_stdev(series, long period=20):
    """ Standard Deviation """

    cdef double[:] xs = asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, s, sx, sxx, vxx, std

    cdef long i, j

    if period > size:
        return result

    for j in range(period-1, size):

        s = sx = sxx = 0.0
        i = j - period + 1

        while i <= j:
            x = xs[i]
            if isnan(x):
                break
            s += 1.0
            sx += x
            sxx += x * x
            i += 1

        else:
            vxx = (sxx / s - sx * sx / s / s)
            std = sqrt(vxx) if vxx >= 0 else NAN
            output[j] = std

    result = wrap_result(result, series)

    return result



class STDEV(Indicator):
    """ Standard Deviation """

    def __init__(self, period : int = 20, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_stdev(series, self.period)
        return result
