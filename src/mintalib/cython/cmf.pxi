""" Chaikin Money Flow """

@add_metadata(inputs=('high', 'low', 'close', 'volume'))
def calc_cmf(high, low, close, volume, long period=20):
    """
    Chaikin Money Flow

    Args:
        period (int): time period, default 20
    """

    if period <= 0:
        raise ValueError("period must be greater than zero")

    high = np.asarray(high, float)
    low = np.asarray(low, float)
    close = np.asarray(close, float)
    volume = np.asarray(volume, float)
    cdef long size = check_size(
        high,
        low,
        close,
        volume,
    )

    spread = high - low
    multiplier = np.zeros(size, float)
    np.divide(
        2 * close - high - low,
        spread,
        out=multiplier,
        where=spread != 0,
    )
    money_flow = multiplier * volume

    numerator = calc_sum(money_flow, period)
    denominator = calc_sum(volume, period)

    with np.errstate(divide='ignore', invalid='ignore'):
        result = numerator / denominator

    return result
