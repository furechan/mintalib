""" Ganeric Moving Average """


@export
def calc_ma(series, long period, *, ma_type: str = None, wrap: bool = True):
    """
    Generic Moving Average

    Args:
        series : data series, required
        period (int) : time period, required
        ma_type (str) : type of moving average, default 'SMA'
            one of 'SMA', 'EMA', 'WMA', 'RMA', 'DEMA', 'TEMA'
    """

    if ma_type is None:
        ma_type= 'SMA'

    if ma_type == 'SMA':
        return calc_sma(series, period, wrap=wrap)

    if ma_type == 'EMA':
        return calc_ema(series, period, wrap=wrap)

    if ma_type == 'WMA':
        return calc_wma(series, period, wrap=wrap)

    if ma_type == 'RMA':
        return calc_rma(series, period, wrap=wrap)

    if ma_type == 'DEMA':
        return calc_dema(series, period, wrap=wrap)

    if ma_type == 'TEMA':
        return calc_tema(series, period, wrap=wrap)

    raise ValueError(f"Invalid ma_type {ma_type}")
