""" Commodity Channel Index """


@add_metadata(inputs=('high', 'low', 'close'))
def calc_cci(prices, long period=20):
    """
    Commodity Channel Index
    
    Args:
        period (int): time period, default 20
    """

    prc = calc_typprice(prices)
    sma = calc_sma(prc, period)
    div = calc_mad(prc, period) * 0.015

    with np.errstate(divide='ignore'):
        result = (prc - sma) / div

    return result
