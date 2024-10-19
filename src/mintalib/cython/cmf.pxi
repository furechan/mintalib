""" Chaiking Money Flow """


def calc_cmf(prices, long period = 20, *, wrap: bool = False):
    """
    Chaikin Money Flow
    
    Args:
        period (int) : time period, default 20
    """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)
    volume = np.asarray(prices['volume'], float)

    size = check_size(high, low, close, volume)

    with np.errstate(divide='ignore', invalid='ignore'):
        mult = (2 * close - high - low) / (high - low) * volume
        num = calc_sum(mult, period)
        div = calc_sum(volume, period)

        result = num / div

    if wrap:
        result = wrap_result(result, prices)

    return result



@wrap_function(calc_cmf)
def CMF(prices, period: int = 20):
    result = calc_cmf(prices, period=period)
    return wrap_result(result, prices)
