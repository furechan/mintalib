""" Bollinger Bands """


bbands_result = namedtuple('bbands_result', 'upperband, middleband, lowerband')


@add_metadata(same_scale=True, output_names=('upperband', 'middleband', 'lowerband'))
def calc_bbands(series, long period=20, double nbdev=2.0):
    """
    Bollinger Bands

    Args:
        period (int): time period, default 20
        nbdev (float): bands width in number of standard deviations
    """

    std = calc_stdev(series, period)

    middle = calc_sma(series, period)

    upper = middle + nbdev * std
    lower = middle - nbdev * std

    result = bbands_result(upper, middle, lower)

    return result


@add_metadata(same_scale=False)
def calc_bbp(series, long period=20, double nbdev=2.0):
    """
    Bollinger Bands Percent (%B)

    Args:
        period (int): time period, default 20
        nbdev (float): bands width in number of standard deviations
    """

    cdef object prc = np.asarray(series, float)

    std = calc_stdev(prc, period)

    middle = calc_sma(prc, period)

    upper = middle + nbdev * std
    lower = middle - nbdev * std

    with np.errstate(divide='ignore', invalid='ignore'):
        result = (prc - lower) / (upper - lower) * 100

    return result



@add_metadata(same_scale=False)
def calc_bbw(series, long period=20, double nbdev=2.0):
    """
    Bollinger Bands Width

    Args:
        period (int): time period, default 20
        nbdev (float): bands width in number of standard deviations
    """

    std = calc_stdev(series, period)

    middle = calc_sma(series, period)

    upper = middle + nbdev * std
    lower = middle - nbdev * std

    with np.errstate(divide='ignore', invalid='ignore'):
        result = (upper - lower) / middle * 100

    return result
