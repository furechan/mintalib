""" Ganeric Moving Average """


def calc_ma(series, long period=20, *, ma_type: str = "SMA", wrap: bool = False):
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


@wrap_function(calc_ma, same_scale=True)
def MA(series, period: int = 20, *, ma_type: str = "SMA", item: str = None):
    series = get_series(series, item=item)
    result = calc_ma(series, period=period, ma_type=ma_type)
    return wrap_result(result, series)

