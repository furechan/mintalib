""" Price Percentage Oscillator """


stoch_result = namedtuple("stoch_result", "slowk, slowd")


@export
def calc_stoch(prices, long period=14, long fastn=3, long slown=3, *, wrap: bool = True):
    """ Stochastik Oscillator """

    cdef double[:] high = np.asarray(prices['high'], float)
    cdef double[:] low = np.asarray(prices['low'], float)
    cdef double[:] close = np.asarray(prices['close'], float)

    cdef long size = check_size(high, low, close)

    hi = calc_max(high, period)
    lo = calc_min(low, period)

    with np.errstate(divide='ignore'):
        fastk = 100 * (close - lo) /(hi - lo)

    slowk = calc_sma(fastk, fastn)
    slowd = calc_sma(slowk, slown)

    result = stoch_result(slowk, slowd)

    if wrap:
        result = wrap_result(result, prices)

    return result



class STOCH(Indicator):
    """ Stockchastic Oscillator """

    def __init__(self, period: int = 14, fastn: int = 3, slown: int = 3, *, item=None):
        self.period = period
        self.fastn = fastn
        self.slown = slown

    def calc(self, prices):
        result = calc_stoch(prices, self.period, self.fastn, self.slown, wrap=True)
        return result


