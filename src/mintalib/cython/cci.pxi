""" Commodity Channel Index """


def calc_cci(prices, long period = 20, *, wrap: bool = False):
    """
    Commodity Channel Index
    
    Args:
        period (int) : time period, default 20
    """

    prc = calc_typprice(prices)
    sma = calc_sma(prc, period)
    div = calc_mad(prc, period) * 0.015

    with np.errstate(divide='ignore'):
        result = (prc - sma) / div

    if wrap:
        result = wrap_result(result, prices)

    return result


@wrap_function(calc_cci)
def CCI(prices, period: int = 20):
    result = calc_cci(prices, period=period)
    return wrap_result(result, prices)
