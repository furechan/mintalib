""" Price """


@with_metadata(same_scale=True)
def calc_price(prices, item: str = None, *, bint wrap=False):
    """ Generic Price 
    
    Args:
        item (str) : one of 'open', 'high', 'low', 'close',
            'avg', 'mid', 'typ', 'wcl' defaults to 'close'
    """

    if item is None:
        item = 'close'

    if item in ('open', 'high', 'low', 'close'):
        result =  np.asarray(prices[item], float)
    elif item in ('avg', 'ohlc4'):
        result = calc_avgprice(prices)
    elif item == ('mid', 'hl2'):
        result = calc_midprice(prices)
    elif item == ('typ', 'hlc3'):
        result = calc_typprice(prices)
    elif item == ('wcl', 'hlcc4'):
        result = calc_wclprice(prices)
    else:
        raise ValueError(f"Unknown price type {item!r}")

    if wrap:
        result = wrap_result(result, prices)

    return result


def calc_avgprice(prices, *, bint wrap=False):
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

    if wrap:
        result = wrap_result(result, prices)

    return result


def calc_typprice(prices, *, bint wrap=False):
    """
    Typical Price

    Value of (high + low + close ) / 3
    """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)

    check_size(high, low, close)

    result = (high + low + close) / 3.0
   
    if wrap:
        result = wrap_result(result, prices)

    return result


def calc_wclprice(prices, *, bint wrap=False):
    """
    Weighted Close Price
    
    Value of (high + low + 2 * close) / 4
    """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)

    check_size(high, low, close)

    result = (high + low + 2 * close) / 4.0

    if wrap:
        result = wrap_result(result, prices)

    return result



def calc_midprice(prices, *, bint wrap=False):
    """
    Mid Price
    
    Value of (high + low) / 2
    """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)

    check_size(high, low)

    result = (high + low) / 2.0

    if wrap:
        result = wrap_result(result, prices)

    return result


