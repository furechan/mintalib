""" Double Exponential Moving Average """

@with_metadata(same_scale=True)
def calc_dema(series, long period, *, bint wrap=False):
    """
    Double Exponential Moving Average
 
    Args:
        period (int) : time period, required    
    """

    ema1 = calc_ema(series, period)
    ema2 = calc_ema(ema1, period)

    result = 2 * ema1 - ema2

    if wrap:
        result = wrap_result(result, series)

    return result

