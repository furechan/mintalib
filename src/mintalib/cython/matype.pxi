""" Ganeric Moving Average """


def calc_ma(series, long period=20, *, ma_type: str = None, wrap: bool = False):
    """Generic Moving Average

    Args:
        matype (str) : one of 'SMA', 'EMA', 'WMA', 'HMA', 'DEMA', 'TEMA'
                defaults to 'SMA'
    """

    if ma_type is None:
        ma_type= 'SMA'

    if ma_type == 'SMA':
        return calc_sma(series, period, wrap=wrap)

    if ma_type == 'EMA':
        return calc_ema(series, period, wrap=wrap)

    if ma_type == 'WMA':
        return calc_wma(series, period, wrap=wrap)

    if ma_type == 'HMA':
        return calc_hma(series, period, wrap=wrap)

    if ma_type == 'DEMA':
        return calc_dema(series, period, wrap=wrap)

    if ma_type == 'TEMA':
        return calc_tema(series, period, wrap=wrap)

    raise ValueError(f"Invalid ma_type {ma_type}")


@wrap_function(calc_ma)
def MA(series, period: int = 20, *, ma_type: str = None, item: str = None):
    series = get_series(series, item=item)
    result = calc_ma(series, period=period, ma_type=ma_type)
    return wrap_result(result, series)

