""" Price """


@add_metadata(same_scale=True)
def calc_price(prices, item: str = None):
    """
    Generic Price

    Args:
        item (str) : price type, one of:
            'open', 'high', 'low', 'close' (default),
            'avg' or 'ohlc4'  — average price (open + high + low + close) / 4,
            'mid' or 'hl2'    — mid price (high + low) / 2,
            'typ' or 'hlc3'   — typical price (high + low + close) / 3,
            'wcl' or 'hlcc4'  — weighted close (high + low + 2 * close) / 4
    """

    if item is None:
        item = 'close'

    if item in ('open', 'high', 'low', 'close'):
        result =  np.asarray(prices[item], float)
    elif item in ('avg', 'ohlc4'):
        result = calc_avgprice(prices)
    elif item in ('mid', 'hl2'):
        result = calc_midprice(prices)
    elif item in ('typ', 'hlc3'):
        result = calc_typprice(prices)
    elif item in ('wcl', 'hlcc4'):
        result = calc_wclprice(prices)
    else:
        raise ValueError(f"Unknown price type {item!r}")

    return result


def calc_avgprice(prices):
    """
    Average Price
    
    Value of (open + high + low + close) / 4
    """

    open = np.asarray(prices['open'], float)
    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)

    check_size(open, high, low, close)

    result = (open + high + low + close) / 4.0

    return result


def calc_typprice(prices):
    """
    Typical Price

    Value of (high + low + close ) / 3
    """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)

    check_size(high, low, close)

    result = (high + low + close) / 3.0
   
    return result


def calc_wclprice(prices):
    """
    Weighted Close Price
    
    Value of (high + low + 2 * close) / 4
    """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)

    check_size(high, low, close)

    result = (high + low + 2 * close) / 4.0

    return result



def calc_midprice(prices):
    """
    Mid Price
    
    Value of (high + low) / 2
    """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)

    check_size(high, low)

    result = (high + low) / 2.0

    return result


