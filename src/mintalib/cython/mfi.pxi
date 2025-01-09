""" Money Flow Index """


def calc_mfi(prices, long period = 14, *, wrap: bool = False):
    """
    Money Flow Index 
    
    Args:
        period (int) : time period, default 14
    """

    prc = calc_typprice(prices)
    volume = np.asarray(prices['volume'], float)

    flow = prc * volume
    pflow = np.clip(flow, 0.0, None)
    nflow = -np.clip(flow, None, 0.0)

    with np.errstate(divide='ignore'):
        ratio = calc_sum(pflow, period) / calc_sum(nflow, period)
        result = 100 - 100 / (1 + ratio)

    if wrap:
        result = wrap_result(result, prices)

    return result

