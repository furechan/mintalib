""" Double Exponential Moving Average """


@export
def calc_dema(series, int period=50):
    """ Double Exponential Moving Average """

    ema1 = calc_ema(series, period)
    ema2 = calc_ema(ema1, period)

    result = 2 * ema1 - ema2

    return result



@export
class DEMA(Indicator):
    """
    Double Exponential Moving Average

    Args:
        period (int) : The indicator period. Default 20

    Returns:
        A Callable
    """

    same_scale = True

    def __init__(self, period: int =20, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_dema(series, self.period)
        return result
