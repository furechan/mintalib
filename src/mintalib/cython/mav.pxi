""" Ganeric Moving Average """


@add_metadata(same_scale=True)
def calc_mav(series, long period=20, *, unicode ma_type = "SMA", bint wrap = False):
    """
    Generic Moving Average

    Moving average computed according to ma_type

    Args:
        ma_type (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
                defaults to 'SMA'
    """

    if ma_type == 'SMA':
        result= calc_sma(series, period)

    elif ma_type == 'EMA':
        result = calc_ema(series, period)

    elif ma_type == 'WMA':
        result = calc_wma(series, period)

    elif ma_type == 'HMA':
        result = calc_hma(series, period)

    elif ma_type == 'DEMA':
        result = calc_dema(series, period)

    elif ma_type == 'TEMA':
        result = calc_tema(series, period)
    else:
        raise ValueError(f"Invalid ma_type {ma_type}")

    if wrap:
        result = wrap_result(result, series)

    return result

