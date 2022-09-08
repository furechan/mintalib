""" Chaiking Money Flow """



@export
def calc_cmf(prices, long period = 20):
    """ Chaikin Money Flow """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)
    volume = np.asarray(prices['volume'], float)

    size = check_size(high, low, close, volume)

    with np.errstate(divide='ignore'):
        mult = (2 * close - high - low) / (high - low) * volume
        num = calc_sum(mult, period)
        div = calc_sum(volume, period)

        result = num / div

    result = wrap_result(result, prices)

    return result


class CMF(Indicator):
    """ Chaikin Money Flow """

    def __init__(self, period: int = 20):
        self.period = period

    def calc(self, prices):
        result = calc_cci(prices, period = self.period)
        return result


