""" Stochastic Oscillator """


stoch_result = namedtuple("stoch_result", "slowk, slowd")

@add_metadata(output_names=('slowk', 'slowd'))
def calc_stoch(prices, long period=14, long fastn=3, long slown=3):
    """
    Stochastic Oscillator
    
    Args:
        period (int) :  time period of window, default, 14
        fastn (int) : time period of fast average, default 3
        slown (int) : time period of slow average, default 3
    """

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

    return result

