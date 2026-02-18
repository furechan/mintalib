""" Triple Exponential Moving Average """

@add_metadata(same_scale=True)
def calc_tema(series, long period=20):
    """
    Triple Exponential Moving Average
    
    Args:
        period (int) : time period, default 20
    """

    ema1 = calc_ema(series, period)
    ema2 = calc_ema(ema1, period)
    ema3 = calc_ema(ema2, period)

    result = 3 * ema1 - 3 * ema2 + ema3

    return result

