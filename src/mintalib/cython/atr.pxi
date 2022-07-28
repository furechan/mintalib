""" True Range """



@export
def calc_trange(prices, *, bint log_prices=False, bint percent=False):
    """ True Range """

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

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double h = NAN, l = NAN, c = NAN, pc = NAN, tr = NAN

    cdef long i = 0

    for i in range(size):
        h = _high[i]
        l = _low[i]
        c = _close[i]

        if isnan(c):
            continue

        if log_prices:
            c = log(c)
            h = log(h)
            l = log(l)

        if pc > h:
            h = pc
        elif pc < l:
            l = pc

        pc = c
        tr = h - l

        if percent:
            tr *= 100 / c

        output[i] = tr

    if isinstance(close, Series):
        result = make_series(result, close)

    return result


@export
def calc_atr(prices, int period=14, *, bint log_prices=False, bint percent=False):
    """ Average True Range """

    trange = calc_trange(prices, log_prices=log_prices, percent=percent)
    atr = calc_rma(trange, period)
    return atr

@export
class ATR(Indicator):
    """ Average Trading Range """

    def __init__(self, period: int = 14):
        self.period = period

    def calc(self, data):
        return calc_atr(data, self.period)


@export
class ATRL(Indicator):
    """ Average Trading Range (logarithmic) """

    def __init__(self, period :int = 14):
        self.period = period

    def calc(self, data):
        return calc_atr(data, self.period, log_prices=True)


@export
class ATRP(Indicator):
    """ Average Trading Range (percent) """

    def __init__(self, period : int = 14):
        self.period = period

    def calc(self, data):
        return calc_atr(data, self.period, percent=True)

