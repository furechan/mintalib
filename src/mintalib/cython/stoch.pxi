""" Stochastic Oscillator """

stoch_result = namedtuple("stoch_result", "slowk, slowd")

@add_metadata(
    output_names=('slowk', 'slowd'),
    inputs=('high', 'low', 'close'),
)
def calc_stoch(high, low, close, long period=14, long fastn=3, long slown=3):
    """
    Stochastic Oscillator

    Args:
        period (int):  time period of window, default, 14
        fastn (int): time period of fast average, default 3
        slown (int): time period of slow average, default 3
    """

    cdef const double[:] high_view = np.asarray(high, float)
    cdef const double[:] low_view = np.asarray(low, float)
    cdef const double[:] close_view = np.asarray(close, float)

    cdef long size = check_size(high_view, low_view, close_view)

    hi = calc_max(high_view, period)
    lo = calc_min(low_view, period)

    with np.errstate(divide='ignore'):
        fastk = 100 * (close_view - lo) / (hi - lo)

    slowk = calc_sma(fastk, fastn)
    slowd = calc_sma(slowk, slown)

    result = stoch_result(slowk, slowd)

    return result
