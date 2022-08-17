""" Triple Exponential Moving Average """


@export
def calc_tema(series, long period=20, wrap: bool = True):
    """ Triple Exponential Moving Average """

    ema1 = calc_ema(series, period, wrap=False)
    ema2 = calc_ema(ema1, period, wrap=False)
    ema3 = calc_ema(ema2, period, wrap=False)

    result = 3 * ema1 - 3 * ema2 + ema3

    if wrap:
        result = wrap_result(result, series)

    return result



class TEMA(Indicator):
    """
    Triple Exponential Moving Average

    Args:
        period (int) : time period. default 20
    """

    same_scale = True

    def __init__(self, period: int = 20, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_tema(series, self.period, wrap=True)
        return result
