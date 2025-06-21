""" Hull Moving Average """


@add_metadata(same_scale=True)
def calc_hma(series, long period, *, bint wrap=False):
    """
    Hull Moving Average

    Args:
        period (int) : time period, required    
    """

    if period <= 0:
        raise ValueError("period must be greater than zero")

    m1 = calc_wma(series, round(period/2))
    m2 = calc_wma(series, period)
    m3 = (2 *  m1) - m2

    result = calc_wma(m3, round(math.sqrt(period)))

    if wrap:
        result = wrap_result(result, series)

    return result

