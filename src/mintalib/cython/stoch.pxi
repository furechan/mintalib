""" Stochastic Oscillator """


stoch_result = namedtuple("stoch_result", "slowk, slowd")

def calc_stoch(prices, long period=14, long fastn=3, long slown=3, *, wrap: bool = False):
    """ Stochastic Oscillator """

    cdef const double[:] high = np.asarray(prices['high'], float)
    cdef const double[:] low = np.asarray(prices['low'], float)
    cdef const double[:] close = np.asarray(prices['close'], float)

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


@wrap_function(calc_stoch)
def STOCH(prices, period: int = 14, fastn: int = 3, slown: int = 3):
    result = calc_stoch(prices, period=period, fastn=fastn, slown=slown)
    return wrap_result(result, prices)

