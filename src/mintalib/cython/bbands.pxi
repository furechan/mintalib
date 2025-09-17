""" Bollinger Bands """


bbands_result = namedtuple('bbands_result', 'upperband, middleband, lowerband')


@add_metadata(same_scale=True, output_names=('upperband', 'middleband', 'lowerband'))
def calc_bbands(prices, long period=20, double nbdev=2.0, *, bint wrap=False):
    """
    Bollinger Bands
    
    Args:
        period (int) : time period, default 20
        nbdev (float) : bands width in number of standard deviations
    """

    prc = calc_typprice(prices)
    std = calc_stdev(prc, period)

    middle = calc_sma(prc, period)

    upper = middle + nbdev * std
    lower = middle - nbdev * std

    result = bbands_result(upper, middle, lower)

    if wrap:
        result = wrap_result(result, prices)

    return result


@add_metadata(same_scale=False)
def calc_bbp(prices, long period=20, double nbdev=2.0, *, bint wrap=False):
    """
    Bollinger Bands Percent (%B)
    
    Args:
        period (int) : time period, default 20
        nbdev (float) : bands width in number of standard deviations
    """

    prc = calc_typprice(prices)
    std = calc_stdev(prc, period)

    middle = calc_sma(prc, period)

    upper = middle + nbdev * std
    lower = middle - nbdev * std

    with np.errstate(divide='ignore', invalid='ignore'):
        result = (prc - lower) / (upper - lower) * 100

    if wrap:
        result = wrap_result(result, prices)

    return result



@add_metadata(same_scale=False)
def calc_bbw(prices, long period=20, double nbdev=2.0, *, bint wrap=False):
    """
    Bollinger Bands Width
    
    Args:
        period (int) : time period, default 20
        nbdev (float) : bands width in number of standard deviations
    """

    prc = calc_typprice(prices)
    std = calc_stdev(prc, period)

    middle = calc_sma(prc, period)

    upper = middle + nbdev * std
    lower = middle - nbdev * std

    with np.errstate(divide='ignore', invalid='ignore'):
        result = (upper - lower) / middle * 100

    if wrap:
        result = wrap_result(result, prices)

    return result
