""" Ganeric Moving Average """

@add_metadata(same_scale=True)
def calc_mav(series, long period=20, *, unicode matype="sma"):
    """
    Generic Moving Average

    Moving average computed according to matype

    Args:
        matype (str): one of 'sma', 'ema', 'wma', 'hma', 'dema', 'tema'
                defaults to 'sma'
    """

    if matype == 'sma':
        result= calc_sma(series, period)

    elif matype == 'ema':
        result = calc_ema(series, period)

    elif matype == 'wma':
        result = calc_wma(series, period)

    elif matype == 'hma':
        result = calc_hma(series, period)

    elif matype == 'dema':
        result = calc_dema(series, period)

    elif matype == 'tema':
        result = calc_tema(series, period)
    else:
        raise ValueError(f"Invalid matype {matype}")

    return result
