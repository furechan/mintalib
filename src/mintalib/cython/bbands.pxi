""" Bollinger Bands """



@export
def calc_bbands(prices, long period = 20, double nbdev = 2.0):
    """ Bollinger Bands """

    prc = calc_typprice(prices)
    std = calc_stdev(prc, period)

    middle = calc_sma(prc, period, wrap=False)

    upper = middle + nbdev * std
    lower = middle - nbdev * std

    result = dict(upperband=upper, middleband=middle, lowerband=lower)

    result = wrap_result(result, prices)

    return result


class BBANDS(Indicator):
    """ Bollinger Bands """

    def __init__(self, period: int = 20, nbdev: float = 2.0):
        self.period = period
        self.nbdev = nbdev

    def calc(self, prices):
        result = calc_bbands(prices, period = self.period, nbdev = self.nbdev)
        return result


