""" Parabolic Stop and Reverse """

@add_metadata(same_scale=True)
def calc_sar(prices, double afs=0.02, double maxaf=0.2):
    """
    Parabolic Stop and Reverse
    
    Args:
        afs (float) : starting acceleration factor, default 0.02
        maxaf (float) : maximum acceleration factor, default 0.2
    """

    cdef const double[:] high = np.asarray(prices['high'], float)
    cdef const double[:] low = np.asarray(prices['low'], float)
    cdef long size = check_size(high, low)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double ep = NAN, sar = NAN, af = NAN
    cdef double hi = NAN, lo = NAN, ph = NAN, pl = NAN, hi2 = NAN, lo2 = NAN

    cdef long i = 0, trend = 0

    for i in range(size):
        if hi >= lo:
            ph, pl = hi, lo

        hi, lo = high[i], low[i]

        if not (hi >= lo and ph >= pl):
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

    return result



