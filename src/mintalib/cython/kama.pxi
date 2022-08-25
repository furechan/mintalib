""" Kaufman Adaptive Moving Average """


@export
def efficiency_ratio(series, int period=10):
    """ Efficiency Ratio """

    cdef double[:] xs = asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x = NAN, px = NAN, dx = NAN
    cdef double y = NAN, py = NAN, dy = NAN

    cdef double erval = NAN, ernum = NAN, erdiv = 0

    cdef long ercnt = 0
    cdef long i = 0, j = 0

    for i in range(size):
        x = xs[i]

        if isnan(x):
            continue

        dx, px = x - px, x

        if isnan(dx):
            continue

        erdiv += fabs(dx)
        ercnt += 1

        while ercnt >= period:
            y, j = xs[j], j+1

            if isnan(y):
                continue

            dy, py = y - py, y

            ernum = fabs(x-y)
            erval = ernum / erdiv if erdiv else 1.0

            if not isnan(dy):
                erdiv -= fabs(dy)
                ercnt -= 1

        output[i] = erval


    return result



@export
def calc_kama(series, int period=10, int fastn=2, int slown=30, wrap: bool = True):
    """ Kaufman Adaptive Moving Average """

    cdef double[:] xs = asarray(series, float)
    cdef double[:] ers = efficiency_ratio(xs, period)

    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double fastf = 2.0 / (fastn + 1.0)
    cdef double slowf = 2.0 / (slown + 1.0)
    cdef double alpha = NAN
    cdef double value = NAN
    cdef double kama = NAN
    cdef double er = NAN

    cdef long i = 0

    for i in range(size):
        value = xs[i]
        er = ers[i]

        if isnan(value) or isnan(er):
            continue

        alpha = (slowf + er * (fastf - slowf)) ** 2.0

        if isnan(kama):
            kama = value
        elif not isnan(alpha):
            kama += alpha * (value - kama)

        output[i] = kama

    if wrap:
        result = wrap_result(result, series)

    return result



@export
class KAMA(Indicator):
    """ Kaufman Adaptative Moving Average """

    same_scale = True

    def __init__(self, period: int=10, fastn: int = 2, slown: int = 30, *, item=None):
        self.period = period
        self.fastn = fastn
        self.slown = slown
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_kama(series, self.period, self.fastn, self.slown, wrap=True)
        return result

