""" Relative Strencgth Index """



@export
def calc_rsi(series, int period=14):
    """ Relative Strength Index """

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double alpha = 1.0 / period
    cdef double v = NAN, pv = NAN, dv = NAN
    cdef double up = NAN, down = NAN, rsi = NAN

    cdef double ups=0.0, downs=0.0
    cdef long i = 0, count = 0

    for i in range(size):
        v = xs[i]

        if isnan(v):
            pass

        elif isnan(pv):
            pv = v

        else:
            count += 1
            dv, pv = v - pv, v
            up, down= (dv, 0.0) if dv >= 0.0 else (0.0, -dv)

            if count <= period:
                ups += up * alpha
                downs += down * alpha
            else:
                ups += (up - ups) * alpha
                downs += (down - downs) * alpha

            if downs > 0 and count >= period:
                rsi = 100.0 - (100.0 / (1.0 + ups / downs))

        if not isnan(rsi):
            output[i] = rsi

    if isinstance(series, Series):
        result = make_series(result, series)

    return result


@export
class RSI(Indicator):
    """ Relative Streng Index """

    def __init__(self, period=14, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_rsi(series, self.period)
        return result

