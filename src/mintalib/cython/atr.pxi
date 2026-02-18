""" Average True Range """


def calc_trange(prices, *, bint log_prices=False, bint percent=False):
    """
    True Range
    
    Args:
        log_prices (bool) : whether to apply log to prices before calculation
        percent (bool) : result as percentage of price
    """

    if log_prices and percent:
        raise ValueError("Only one of log_prices and percent can be true")

    cdef const double[:] high = np.asarray(prices['high'], float)
    cdef const double[:] low = np.asarray(prices['low'], float)
    cdef const double[:] close = np.asarray(prices['close'], float)

    cdef long size = check_size(high, low, close)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double hi = NAN, lo = NAN, cl = NAN, pc = NAN, tr = NAN

    cdef long i = 0

    for i in range(size):
        hi, lo, cl, pc = high[i], low[i], close[i], cl

        if not (hi >= lo > 0.0):
            continue

        if pc > hi:
            hi = pc

        if pc < lo:
            lo = pc

        if log_prices:
            tr = math.log(hi) - math.log(lo)
        elif percent:
            tr = 100 * (hi - lo) / cl if cl > 0 else np.nan
        else:
            tr = (hi - lo)

        output[i] = tr

    return result



def calc_atr(prices, long period=14):
    """
    Average True Range
    
    Args:
        period (int) : time period, default 14    
    """

    trange = calc_trange(prices)
    result = calc_rma(trange, period)

    return result



def calc_natr(prices, long period=14):
    """
    Average True Range (normalized)
    
    Args:
        period (int) : time period, default 14    
    """

    trange = calc_trange(prices, percent=True)
    result = calc_rma(trange, period)

    return result


