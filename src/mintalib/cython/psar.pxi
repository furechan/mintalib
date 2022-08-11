""" exponential moving average """


@export
def calc_psar(prices, double afs=0.02, double maxaf=0.2):
    """ Parabolic SAR """

    high, low = extract_items(prices, ('high', 'low'))

    cdef double[:] _high = np.asarray(high, float)
    cdef double[:] _low = np.asarray(low, float)

    cdef long size = _high.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double ep = NAN, sar = NAN, af = NAN
    cdef double hi = NAN, lo = NAN, ph = NAN, pl = NAN, hi2 = NAN, lo2 = NAN

    cdef long i = 0, trend = 0
    cdef bint valid = False

    for i in range(size):
        if valid:
            ph, pl = hi, lo

        hi, lo = _high[i], _low[i]

        valid = (hi >= lo)

        if not valid:
            continue

        if isnan(ph) or isnan(pl):
            continue

        hi2 = ph if ph > hi else hi
        lo2 = pl if pl < lo else lo

        # check for reversal
        if trend > 0 and lo < sar:
            ep, sar, af, trend = lo, ep, afs, -1

        elif trend < 0 and hi > sar:
            ep, sar, af, trend = hi, ep, afs, +1

        output[i] = sar

        # calculate next sar

        if trend == 0:
            # initialize sar
            if hi > ph:
                ep, sar, af, trend = hi2, lo2, afs, +1
            else:
                ep, sar, af, trend = lo2, hi2, afs, -1
        else:
            # update sar
            sar += af * (ep - sar)

            # adjust sar, ep, af if needed
            if trend > 0:
                if lo2 < sar:
                    sar = lo2
                if hi > ep:
                    ep = hi
                    af += afs
            if trend < 0:
                if hi2 > sar:
                    sar = hi2
                if lo < ep:
                    ep = lo
                    af += afs

        if maxaf and af > maxaf:
            af = maxaf

    if isinstance(prices, DataFrame):
        result = make_series(result, prices)

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

