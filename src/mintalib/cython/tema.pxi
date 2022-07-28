""" Triple Exponential Moving Average """


@export
def calc_tema(series, int period=20):
    """ Triple Exponential Moving Average """

    ema1 = calc_ema(series, period)
    ema2 = calc_ema(ema1, period)
    ema3 = calc_ema(ema2, period)

    result = 3 * ema1 - 3 * ema2 + ema3

    return result


@export
class TEMA(Indicator):
    """
    Triple Exponential Moving Average

    Args:
        period (int) : The indicator period. Default 20

    Returns:
        A Callable
    """

    same_scale = True

    def __init__(self, period: int = 20, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_tema(series, self.period)
        return result
