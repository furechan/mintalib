""" ADX """


@export
def calc_plus_di(prices, int period=14):
    """ PLUS DI """

    high, low = extract_items(prices, ('high', 'low'))

    atr = calc_atr(prices, period)

    hm = calc_diff(high, 1)
    lm = -calc_diff(low, 1)
    dm = np.where((hm > lm) & (hm > 0), hm, 0)

    with np.errstate(divide='ignore'):
        result = 100 * calc_rma(dm, period) / atr

    if isinstance(prices, DataFrame):
        result = make_series(result, prices)

    return result


@export
def calc_minus_di(prices, int period=14):
    """ MINUS DI """

    high, low = extract_items(prices, ('high', 'low'))

    atr = calc_atr(prices, period)

    hm = calc_diff(high, 1)
    lm = -calc_diff(low, 1)
    dm = np.where((lm > hm) & (lm > 0), lm, 0)

    with np.errstate(divide='ignore'):
        result = 100 * calc_rma(dm, period) / atr

    if isinstance(prices, DataFrame):
        result = make_series(result, prices)

    return result


@export
def calc_adx(prices, int period=14):
    """ ADX """

    high, low = extract_items(prices, ('high', 'low'))

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

    if isinstance(prices, DataFrame):
        result = make_series(result, prices)

    return result


@export
class ADX(Indicator):
    """ ADX """

    def __init__(self, period: int = 14):
        self.period = period

    def calc(self, data):
        return calc_adx(data, self.period)
