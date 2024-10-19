""" Average True Range """


def calc_trange(prices, *, log_prices: bool = False, percent: bool = False, wrap: bool = False):
    """
    True Range
    
    Args:
        log_percent (bool) : whether to apply log to prices before calculatio
        percent (bool) : result as percentage of price
    """

    cdef const double[:] high = np.asarray(prices['high'], float)
    cdef const double[:] low = np.asarray(prices['low'], float)
    cdef const double[:] close = np.asarray(prices['close'], float)

    cdef long size = check_size(high, low, close)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double hi = NAN, lo = NAN, cl = NAN, pc = NAN, tr = NAN

    cdef long i = 0

    cdef bint use_log = log_prices
    cdef bint use_percent = percent

    for i in range(size):
        pc, hi, lo, cl = cl, high[i], low[i], close[i]

        if not (pc > 0.0 and cl > 0.0 and hi > lo > 0.0):
            continue

        if pc > hi:
            hi = pc

        if pc < lo:
            lo = pc

        if use_log:
            tr = math.log(hi) - math.log(lo)
        elif use_percent:
            tr = 100 * (hi - lo) / cl
        else:
            tr = (hi - lo)

        output[i] = tr

    if wrap:
        result = wrap_result(result, prices)

    return result



def calc_atr(prices, long period=14, *, wrap: bool = False):
    """
    Average True Range
    
    Args:
        period (int) : time period, default 14    
    """

    trange = calc_trange(prices)
    result = calc_rma(trange, period)

    if wrap:
        result = wrap_result(result, prices)

    return result



def calc_natr(prices, long period=14, *, wrap: bool = False):
    """
    Average True Range (normalized)
    
    Args:
        period (int) : time period, default 14    
    """

    trange = calc_trange(prices, percent=True)
    result = calc_rma(trange, period)

    if wrap:
        result = wrap_result(result, prices)

    return result



@wrap_function(calc_trange)
def TRANGE(prices, *, log_prices: bool = False, percent: bool = False):
    result = calc_trange(prices, log_prices=log_prices, percent=percent)
    return wrap_result(result, prices)


@wrap_function(calc_atr)
def ATR(prices, period: int = 14):
    result = calc_atr(prices, period=period)
    return wrap_result(result, prices)


@wrap_function(calc_natr)
def NATR(prices, period: int = 14):
    result = calc_natr(prices, period=period)
    return wrap_result(result, prices)

