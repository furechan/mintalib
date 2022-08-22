""" Commodity Channel Index """



@export
def calc_cci(prices, long period = 20):
    """ Commodity Channel Index """

    prc = calc_typprice(prices)
    sma = calc_sma(prc, period, wrap=False)
    div = calc_mad(prc, period) * 0.015

    with np.errstate(divide='ignore'):
        result = (prc - sma) / div

    result = wrap_result(result, prices)

    return result


class CCI(Indicator):
    """ Commodity Channel Index """

    def __init__(self, period: int = 20):
        self.period = period

    def calc(self, prices):
        result = calc_cci(prices, period = self.period)
        return result


