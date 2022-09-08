""" Average True Range """


@export
def calc_trange(prices, *, log_prices: bool = False, percent: bool = False, wrap: bool = True):
    """ True Range """

    cdef double[:] high = np.asarray(prices['high'], float)
    cdef double[:] low = np.asarray(prices['low'], float)
    cdef double[:] close = np.asarray(prices['close'], float)

    cdef long size = check_size(high, low, close)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double hi = NAN, lo = NAN, cl = NAN, pc = NAN, tr = NAN

    cdef long i = 0

    cdef bint use_log = log_prices
    cdef bint use_percent = percent

    for i in range(size):
        pc, hi, lo, cl = cl, high[i], low[i], close[i]

        if not (pc > 0.0 and cl > 0.0 and hi > lo > 0.0):
            continue

        if pc > hi:
            hi = pc

        if pc < lo:
            lo = pc

        if use_log:
            tr = log(hi) - log(lo)
        elif use_percent:
            tr = 100 * (hi - lo) / cl
        else:
            tr = (hi - lo)

        output[i] = tr

    if wrap:
        result = wrap_result(result, prices)

    return result


@export
def calc_atr(prices, long period=14):
    """ Average True Range """

    trange = calc_trange(prices)
    result = calc_rma(trange, period, wrap=False)

    result = wrap_result(result, prices)

    return result


@export
def calc_natr(prices, long period=14):
    """ Average True Range (normalized) """

    trange = calc_trange(prices, percent=True)
    result = calc_rma(trange, period, wrap=False)

    result = wrap_result(result, prices)

    return result


@export
def calc_latr(prices, long period=14):
    """ Average True Range (logarithmic) """

    cdef bint yes = True

    trange = calc_trange(prices, log_prices=True)
    result = calc_rma(trange, period, wrap=False)

    result = wrap_result(result, prices)

    return result



class TRANGE(Indicator):
    """ True Range """

    def __init__(self):
        pass

    def calc(self, data):
        return calc_trange(data, wrap=True)


class ATR(Indicator):
    """ Average True Range """

    def __init__(self, period: int = 14):
        self.period = period

    def calc(self, data):
        return calc_atr(data, self.period)


class NATR(Indicator):
    """ Average True Range (normalized) """

    def __init__(self, period : int = 14):
        self.period = period

    def calc(self, data):
        return calc_natr(data, self.period)

class LATR(Indicator):
    """ Average True Range (log prices) """

    def __init__(self, period : int = 14):
        self.period = period

    def calc(self, data):
        return calc_latr(data, self.period)


