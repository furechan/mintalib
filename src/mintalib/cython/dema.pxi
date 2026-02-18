""" Double Exponential Moving Average """

@add_metadata(same_scale=True)
def calc_dema(series, long period):
    """
    Double Exponential Moving Average
 
    Args:
        period (int) : time period, required    
    """

    ema1 = calc_ema(series, period)
    ema2 = calc_ema(ema1, period)

    result = 2 * ema1 - ema2

    return result

