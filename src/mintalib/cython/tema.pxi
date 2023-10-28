""" Triple Exponential Moving Average """

def calc_tema(series, long period=20, *, wrap: bool = False):
    """
    Triple Exponential Moving Average

    Args:
        period (int) : time period. default 20
    """

    ema1 = calc_ema(series, period)
    ema2 = calc_ema(ema1, period)
    ema3 = calc_ema(ema2, period)

    result = 3 * ema1 - 3 * ema2 + ema3

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(calc_tema)
def TEMA(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_tema(series, period=period)
    return wrap_result(result, series)


