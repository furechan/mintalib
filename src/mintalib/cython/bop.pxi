""" Balance of Power """


def calc_bop(prices, long period=20):
    """
    Balance of Power
    
    Args:
        period (int) : time period, default 20
    """

    open = np.asarray(prices['open'], float)
    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)

    size = check_size(open, high, low, close)

    with np.errstate(all='ignore'):
        bop = (close - open) / (high - low)
        result = calc_sma(bop, period)

    return result

