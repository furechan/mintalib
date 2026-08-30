""" Keltner Channel """

keltner_result = namedtuple('keltner_result', 'upperband, middleband, lowerband')

@add_metadata(
    same_scale=True,
    output_names=('upperband', 'middleband', 'lowerband'),
    inputs=('high', 'low', 'close'),
)
def calc_keltner(high, low, close, long period=20, double nbatr=2.0):
    """
    Keltner Channel

    Args:
        period (int): time period, default 20
        nbatr (float): channel width in number of atrs, default 2.0
    """

    prc = calc_typprice(high, low, close)
    atr = calc_atr(high, low, close, period)

    middle = calc_ema(prc, period)
    upper = middle + nbatr * atr
    lower = middle - nbatr * atr

    result = keltner_result(upper, middle, lower)

    return result
