""" Balance of Power """



@export
def calc_bop(prices, long period = 20):
    """ Balance of Power """

    open = np.asarray(prices['open'], float)
    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)

    size = check_size(open, high, low, close)

    with np.errstate(all='ignore'):
        bop = (close - open) / (high - low)
        result = calc_sma(bop, period)

    result = wrap_result(result, prices)

    return result


class BOP(Indicator):
    """ Balance of Power """

    def __init__(self, period: int = 20):
        self.period = period

    def calc(self, prices):
        result = calc_bop(prices, period = self.period)
        return result


