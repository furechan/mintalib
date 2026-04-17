""" Donchian Channel """

donchian_result = namedtuple('donchian_result', 'upperband, middleband, lowerband')

@add_metadata(same_scale=True, output_names=('upperband', 'middleband', 'lowerband'))
def calc_donchian(prices, long period=20):
    """
    Donchian Channel

    Args:
        period (int) : time period, default 20
    """

    upper = calc_max(prices['high'], period)
    lower = calc_min(prices['low'], period)
    middle = (upper + lower) / 2

    result = donchian_result(upper, middle, lower)

    return result
