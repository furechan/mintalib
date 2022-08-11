""" True Range """

@export
def calc_trange(prices, *, bint log_prices=False, bint percent=False):
    """ True Range """

    high, low, close = extract_items(prices, ('high', 'low', 'close'))

    cdef double[:] _high = np.asarray(high, float)
    cdef double[:] _low = np.asarray(low, float)
    cdef double[:] _close = np.asarray(close, float)

    cdef long size = _close.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double h = NAN, l = NAN, c = NAN, pc = NAN, tr = NAN

    cdef long i = 0

    for i in range(size):
        pc, h, l, c = c, _high[i], _low[i], _close[i]

        if isnan(c) or isnan(pc):
            continue

        if pc > h:
            h = pc

        if pc < l:
            l = pc

        if log_prices:
            if h > 0 and l > 0:
                tr = log(h) - log(l)
            else:
                tr = np.nan
        else:
            tr = h - l

        if percent:
            tr = 100 * tr / c if c > 0 else np.nan

        output[i] = tr

    if isinstance(prices, DataFrame):
        result = make_series(result, prices)

    return result


@export
def calc_atr(prices, int period=14, *, bint log_prices=False, bint percent=False):
    """ Average True Range """

    trange = calc_trange(prices, log_prices=log_prices, percent=percent)
    result = calc_rma(trange, period)
    return result



@export
def calc_natr(prices, int period=14):
    """ Normalized Average True Range """

    return calc_atr(prices, period=period, percent=True)


@export
class ATR(Indicator):
    """ Average Trading Range """

    def __init__(self, period: int = 14):
        self.period = period

    def calc(self, data):
        return calc_atr(data, self.period)


@export
class NATR(Indicator):
    """ Average Trading Range (percent) """

    def __init__(self, period : int = 14):
        self.period = period

    def calc(self, data):
        return calc_natr(data, self.period)

