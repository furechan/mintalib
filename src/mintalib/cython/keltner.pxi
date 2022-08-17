""" Keltner Bands """



@export
def calc_keltner(prices, long period = 20, double nbatr = 2.0):
    """ Keltner Bands """

    prc = calc_typprice(prices)
    atr = calc_atr(prices, period / 2)

    middle = calc_ema(prc, period, wrap=False)
    upper = middle + nbatr * atr
    lower = middle - nbatr * atr

    result = dict(
        upperband=upper,
        middleband=middle,
        lowerband=lower
    )

    result = wrap_result(result, prices)

    return result



class KELTNER(Indicator):
    """ Keltner Bands """

    def __init__(self, period: int = 20, nbatr: float = 2.0):
        self.period = period
        self.nbatr = nbatr

    def calc(self, prices):
        result = calc_keltner(prices, period = self.period, nbatr = self.nbatr)
        return result


