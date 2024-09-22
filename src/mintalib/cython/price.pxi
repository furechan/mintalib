""" Price """


def calc_avgprice(prices, *, wrap: bool = False):
    """ Average Price """

    cdef const double[:] open = np.asarray(prices['open'], float)
    cdef const double[:] high = np.asarray(prices['high'], float)
    cdef const double[:] low = np.asarray(prices['low'], float)
    cdef const double[:] close = np.asarray(prices['close'], float)

    cdef long size = check_size(open, high, low, close)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (open[i] + high[i] + low[i] + close[i]) / 4.0
        output[i] = v

    if wrap:
        result = wrap_result(result, prices)

    return result


def calc_typprice(prices, *, wrap: bool = False):
    """ Typical Price """

    cdef double[:] high = np.asarray(prices['high'], float)
    cdef double[:] low = np.asarray(prices['low'], float)
    cdef double[:] close = np.asarray(prices['close'], float)

    cdef long size = check_size(high, low, close)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (high[i] + low[i] + close[i]) / 3.0
        output[i] = v

    if wrap:
        result = wrap_result(result, prices)

    return result


def calc_wclprice(prices, *, wrap: bool = False):
    """ Weighted Close Price """

    cdef double[:] high = np.asarray(prices['high'], float)
    cdef double[:] low = np.asarray(prices['low'], float)
    cdef double[:] close = np.asarray(prices['close'], float)

    cdef long size = check_size(high, low, close)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (high[i] + low[i] + 2 * close[i]) / 4.0
        output[i] = v

    if wrap:
        result = wrap_result(result, prices)

    return result



def calc_midprice(prices, *, wrap: bool = False):
    """ Mid Price """

    cdef double[:] high = np.asarray(prices['high'], float)
    cdef double[:] low = np.asarray(prices['low'], float)
    cdef long size = check_size(high, low)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (high[i] + low[i]) / 2.0
        output[i] = v

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
        result =  np.asarray(prices[item], float)
        if wrap:
            result = wrap_result(result, prices)
        return result

    if item == 'avg':
        price_func = calc_avgprice
    elif item == 'mid':
        price_func = calc_midprice
    elif item == 'typ':
        price_func = calc_typprice
    elif item == 'wcl':
        price_func = calc_wclprice
    else:
        raise ValueError(f"Unknown price type {item!r}")

    return price_func(prices, wrap=wrap)



@wrap_function(calc_avgprice)
def AVGPRICE(prices):
    result = calc_avgprice(prices)
    return wrap_result(result, prices)


@wrap_function(calc_typprice)
def TYPPRICE(prices):
    result = calc_typprice(prices)
    return wrap_result(result, prices)


@wrap_function(calc_wclprice)
def WCLPRICE(prices):
    result = calc_wclprice(prices)
    return wrap_result(result, prices)


@wrap_function(calc_midprice)
def MIDPRICE(prices):
    result = calc_midprice(prices)
    return wrap_result(result, prices)


@wrap_function(calc_price)
def PRICE(prices, item: str = None):
    result = calc_price(prices, item=item)
    return wrap_result(result, prices)

