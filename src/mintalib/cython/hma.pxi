""" Hull Moving Average """



def calc_hma(series, long period = 20, *, wrap: bool = False):
    """Hull Moving Average"""

    if period <= 0:
        raise ValueError("period must be greater than zero")

    m1 = calc_wma(series, round(period/2))
    m2 = calc_wma(series, period)
    m3 = (2 *  m1) - m2

    result = calc_wma(m3, round(math.sqrt(period)))

    if wrap:
        result = wrap_result(result, series)

    return result



@wrap_function(calc_hma)
def HMA(series, period: int, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_hma(series, period=period)
    return wrap_result(result, series)

