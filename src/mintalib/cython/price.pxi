""" Price """


def calc_avgprice(prices, *, wrap: bool = False):
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


def calc_typprice(prices, *, wrap: bool = False):
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


def calc_wclprice(prices, *, wrap: bool = False):
    """
    Weighted Close Price
    
    Value of (high + low + 2 * close) / 3
    """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)
    close = np.asarray(prices['close'], float)

    check_size(high, low, close)

    result = (high + low + 2 * close) / 4.0

    if wrap:
        result = wrap_result(result, prices)

    return result



def calc_midprice(prices, *, wrap: bool = False):
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


def calc_price(prices, item: str = None, *, wrap: bool = False):
    """ Generic Price 
    
    Args:
        item (str) : one of 'open', 'high', 'low', 'close',
            'avg', 'mid', 'typ', 'wcl' defaults to 'close'
    """

    if item is None:
        item = 'close'

    if item in ('open', 'high', 'low', 'close'):
        result =  np.asarray(prices[item], np.float64)
    elif item == 'avg':
        result = calc_avgprice(prices)
    elif item == 'mid':
        result = calc_midprice(prices)
    elif item == 'typ':
        result = calc_typprice(prices)
    elif item == 'wcl':
        result = calc_wclprice(prices)
    else:
        raise ValueError(f"Unknown price type {item!r}")

    if wrap:
        result = wrap_result(result, prices)

    return result



@wrap_function(calc_avgprice, same_scale=True)
def AVGPRICE(prices):
    result = calc_avgprice(prices)
    return wrap_result(result, prices)


@wrap_function(calc_typprice, same_scale=True)
def TYPPRICE(prices):
    result = calc_typprice(prices)
    return wrap_result(result, prices)


@wrap_function(calc_wclprice, same_scale=True)
def WCLPRICE(prices):
    result = calc_wclprice(prices)
    return wrap_result(result, prices)


@wrap_function(calc_midprice, same_scale=True)
def MIDPRICE(prices):
    result = calc_midprice(prices)
    return wrap_result(result, prices)


@wrap_function(calc_price, same_scale=True)
def PRICE(prices, item: str = None):
    result = calc_price(prices, item=item)
    return wrap_result(result, prices)

