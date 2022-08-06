""" ADX """


@export
def calc_adx(prices, int period=14):
    """ ADX """

    if isinstance(prices, tuple):
        high, low, close = prices
    else:
        high = prices['high']
        low = prices['low']
        close = prices['close']

    atr = calc_atr(prices, period)

    hm = high.diff()
    lm = -low.diff()

    dm1 = np.where((hm > lm) & (hm > 0), hm, 0)
    dm2 = np.where((lm > hm) & (lm > 0), lm, 0)

    with np.errstate(divide='ignore'):
        di1 = 100 * calc_rma(dm1, period) / atr
        di2 = 100 * calc_rma(dm2, period) / atr
        dx = 100 * np.abs(di1 - di2) / (di1 + di2)

    adx = calc_rma(dx, period)

    return adx


@export
class ADX(Indicator):
    """ ADX """

    def __init__(self, period: int = 14):
        self.period = period

    def calc(self, data):
        return calc_adx(data, self.period)

