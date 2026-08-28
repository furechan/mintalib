""" Balance of Power """


def calc_bop(prices):
    """
    Balance of Power
    """

    open = np.asarray(prices['open'], float)
    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)

    size = check_size(open, high, low, close)

    spread = high - low
    result = np.full(size, np.nan)
    np.divide(close - open, spread, out=result, where=spread != 0)

    return result
