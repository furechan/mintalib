""" Average Directional Index """



def calc_plusdi(prices, long period=14, *, wrap: bool = False):
    """ Plus Directional Index """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    atr = calc_atr(prices, period)

    hm = calc_diff(high, 1)
    lm = -calc_diff(low, 1)
    dm = np.where((hm > lm) & (hm > 0), hm, 0)

    with np.errstate(divide='ignore'):
        result = 100 * calc_rma(dm, period) / atr

    if wrap:
        result = wrap_result(result, prices)

    return result



def calc_minusdi(prices, long period=14, *, wrap: bool = False):
    """ Minus Directional Index """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    atr = calc_atr(prices, period)

    hm = calc_diff(high, 1)
    lm = -calc_diff(low, 1)
    dm = np.where((lm > hm) & (lm > 0), lm, 0)

    with np.errstate(divide='ignore'):
        result = 100 * calc_rma(dm, period) / atr

    if wrap:
        result = wrap_result(result, prices)

    return result



def calc_adx(prices, long period=14, *, wrap: bool = False):
    """ Average Directional Index """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)

    atr = calc_atr(prices, period)

    hm = calc_diff(high, 1)
    lm = -calc_diff(low, 1)

    dm1 = np.where((hm > lm) & (hm > 0), hm, 0)
    dm2 = np.where((lm > hm) & (lm > 0), lm, 0)

    with np.errstate(divide='ignore'):
        di1 = 100 * calc_rma(dm1, period) / atr
        di2 = 100 * calc_rma(dm2, period) / atr
        dx = 100 * np.abs(di1 - di2) / (di1 + di2)

    result = calc_rma(dx, period)

    if wrap:
        result = wrap_result(result, prices)

    return result


@wrap_function(calc_plusdi)
def PLUSDI(prices, period: int = 14):
    result = calc_plusdi(prices, period=period)
    return wrap_result(result, prices)


@wrap_function(calc_minusdi)
def MINUSDI(prices, period: int = 14):
    result = calc_minusdi(prices, period=period)
    return wrap_result(result, prices)


@wrap_function(calc_adx)
def ADX(prices, period: int = 14):
    result = calc_adx(prices, period=period)
    return wrap_result(result, prices)

