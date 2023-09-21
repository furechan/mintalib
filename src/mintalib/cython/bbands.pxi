""" Bollinger Bands """


bbands_result = namedtuple('bbands_result', 'upperband, middleband, lowerband')


def calc_bbands(prices, long period = 20, double nbdev = 2.0, *, wrap: bool = False):
    """ Bollinger Bands """

    prc = calc_typprice(prices)
    std = calc_stdev(prc, period)

    middle = calc_sma(prc, period)

    upper = middle + nbdev * std
    lower = middle - nbdev * std

    result = bbands_result(upper, middle, lower)

    if wrap:
        result = wrap_result(result, prices)

    return result


@wrap_function(calc_bbands)
def BBANDS(prices, period: int = 20, nbdev: float = 2.0):
    result = calc_bbands(prices, period=period, nbdev=nbdev)
    return wrap_result(result, prices)

