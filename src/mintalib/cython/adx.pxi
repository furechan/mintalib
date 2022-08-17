""" Average Directional Index """


@export
def calc_plusdi(prices, long period=14):
    """ Plus Directional Index """

    high = asarray(prices['high'], float)
    low = asarray(prices['low'], float)
    atr = calc_atr(prices, period)

    hm = calc_diff(high, 1)
    lm = -calc_diff(low, 1)
    dm = np.where((hm > lm) & (hm > 0), hm, 0)

    with np.errstate(divide='ignore'):
        result = 100 * calc_rma(dm, period, wrap=False) / atr

    result = wrap_result(result, prices)

    return result


@export
def calc_minusdi(prices, long period=14):
    """ Minus Directional Index """

    high = asarray(prices['high'], float)
    low = asarray(prices['low'], float)
    atr = calc_atr(prices, period)

    hm = calc_diff(high, 1)
    lm = -calc_diff(low, 1)
    dm = np.where((lm > hm) & (lm > 0), lm, 0)

    with np.errstate(divide='ignore'):
        result = 100 * calc_rma(dm, period, wrap=False) / atr

    result = wrap_result(result, prices)

    return result


@export
def calc_adx(prices, long period=14):
    """ Average Directional Index """

    high = asarray(prices['high'], float)
    low = asarray(prices['low'], float)

    atr = calc_atr(prices, period)

    hm = calc_diff(high, 1)
    lm = -calc_diff(low, 1)

    dm1 = np.where((hm > lm) & (hm > 0), hm, 0)
    dm2 = np.where((lm > hm) & (lm > 0), lm, 0)

    with np.errstate(divide='ignore'):
        di1 = 100 * calc_rma(dm1, period, wrap=False) / atr
        di2 = 100 * calc_rma(dm2, period, wrap=False) / atr
        dx = 100 * np.abs(di1 - di2) / (di1 + di2)

    result = calc_rma(dx, period, wrap=False)

    result = wrap_result(result, prices)

    return result


class ADX(Indicator):
    """ Average Directional Index """

    def __init__(self, period: int = 14):
        self.period = period

    def calc(self, data):
        return calc_adx(data, self.period)

class PLUSDI(Indicator):
    """ Plus Directional Index """

    def __init__(self, period: int = 14):
        self.period = period

    def calc(self, data):
        return calc_plusdi(data, self.period)

class MINUSDI(Indicator):
    """ Minus Directional Index """

    def __init__(self, period: int = 14):
        self.period = period

    def calc(self, data):
        return calc_minusdi(data, self.period)
