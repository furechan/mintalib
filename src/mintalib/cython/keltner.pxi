""" Keltner Channel """

keltner_result = namedtuple('keltner_result', 'upperband, middleband, lowerband')

def calc_keltner(prices, long period = 20, double nbatr = 2.0, *, wrap: bool = False):
    """ Keltner Channel """

    prc = calc_typprice(prices)
    atr = calc_atr(prices, period / 2)

    middle = calc_ema(prc, period)
    upper = middle + nbatr * atr
    lower = middle - nbatr * atr

    result = keltner_result(upper, middle, lower)

    if wrap:
        result = wrap_result(result, prices)

    return result


@wrap_function(calc_keltner)
def KELTNER(prices, period: int = 20, nbatr: float = 2.0):
    result = calc_keltner(prices, period=period, nbatr=nbatr)
    return wrap_result(result, prices)

