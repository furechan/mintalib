""" Balance of Power """


def calc_bop(prices, long period = 20, *, wrap: bool = False):
    """ Balance of Power """

    open = np.asarray(prices['open'], float)
    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)

    size = check_size(open, high, low, close)

    with np.errstate(all='ignore'):
        bop = (close - open) / (high - low)
        result = calc_sma(bop, period)

    if wrap:
        result = wrap_result(result, prices)

    return result


@wrap_function(calc_bop)
def BOP(prices, period: int = 20):
    result = calc_bop(prices, period=period)
    return wrap_result(result, prices)

