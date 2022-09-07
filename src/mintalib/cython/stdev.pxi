""" Standard Deviation """


@export
def calc_stdev(series, long period=20):
    """ Standard Deviation """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, s, sx, sxx, vxx, std

    cdef long i = 0, j = 0

    cdef long maxlen = size - period + 1

    for i in range(maxlen):

        s = sx = sxx = 0.0

        for j in range(period):
            x = xs[i + j]

            if isnan(x):
                break

            s += 1.0
            sx += x
            sxx += x * x

        else:
            vxx = (sxx / s - sx * sx / s / s)
            std = sqrt(vxx) if vxx >= 0 else NAN
            output[i + j] = std

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
