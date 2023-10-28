""" Double Exponential Moving Average """


def calc_dema(series, long period, wrap: bool = False):
    """ Double Exponential Moving Average """

    ema1 = calc_ema(series, period)
    ema2 = calc_ema(ema1, period)

    result = 2 * ema1 - ema2

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(calc_dema)
def DEMA(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_dema(series, period=period)
    return wrap_result(result, series)

