""" exponential moving average """


@export
def calc_psar(prices, double afs=0.02, double maxaf=0.2):
    """ Parabolic SAR """

    if isinstance(prices, tuple):
        high, low, close = prices
    else:
        high = prices['high']
        low = prices['low']
        close = prices['close']

    cdef double[:] _high = np.asarray(high, float)
    cdef double[:] _low = np.asarray(low, float)
    cdef double[:] _close = np.asarray(close, float)

    cdef long size = _close.size

    cdef object result = np.full(size, np.nan, dtype=float)
    cdef double[:] output = result

    cdef double sar = NAN, ep = NAN, af = NAN
    cdef double hi = NAN, lo = NAN

    cdef long direction = 0
    cdef long i = 0

    for i in range(size):
        hi, lo = _high[i], _low[i]

        if not direction:
            sar, ep, af = lo, hi, afs
            direction = +1

        elif direction > 0 and lo < sar:
            sar, ep, af = ep, hi, afs
            direction = -1

        elif direction < 0 and hi > sar:
            sar, ep, af = ep, lo, afs
            direction = +1

        output[i] = sar

        sar += af * (ep-sar)

        if direction > 0 and hi > ep:
            af += afs
            ep = hi

        if direction < 0 and lo < ep:
            af += afs
            ep = lo

        if maxaf and af > maxaf:
            af = maxaf

    if isinstance(close, Series):
        result = make_series(result, close)

    return result


@export
class PSAR(Indicator):
    """ Parabolic Stop and Reverse (cf Wilder) """

    def __init__(self, afs=0.02, maxaf=0.2):
        self.afs = afs
        self.maxaf = maxaf

    def calc(self, data):
        result = calc_psar(data, afs=self.afs, maxaf=self.maxaf)
        return result

