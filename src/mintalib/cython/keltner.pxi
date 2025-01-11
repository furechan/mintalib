""" Keltner Channel """

keltner_result = namedtuple('keltner_result', 'upperband, middleband, lowerband')

@with_metadata(same_scale=True)
def calc_keltner(prices, long period = 20, double nbatr = 2.0, *, bint wrap=False):
    """
    Keltner Channel
    
    Args:
        period (int) : time period, default 20
        nbatr (float) : channel width in number of atrs, default 2.0
    """

    prc = calc_typprice(prices)
    atr = calc_atr(prices, period)

    middle = calc_ema(prc, period)
    upper = middle + nbatr * atr
    lower = middle - nbatr * atr

    result = keltner_result(upper, middle, lower)

    if wrap:
        result = wrap_result(result, prices)

    return result
