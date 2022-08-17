""" Double Exponential Moving Average """


@export
def calc_dema(series, long period, wrap: bool = True):
    """ Double Exponential Moving Average """

    ema1 = calc_ema(series, period, wrap=False)
    ema2 = calc_ema(ema1, period, wrap=False)

    result = 2 * ema1 - ema2

    if wrap:
        result = wrap_result(result, series)

    return result


class DEMA(Indicator):
    """
    Double Exponential Moving Average

    Args:
        period (int) : time period, default 20
    """

    same_scale = True

    def __init__(self, period: int, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_dema(series, self.period, wrap=True)
        return result
