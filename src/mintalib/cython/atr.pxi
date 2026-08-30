""" Average True Range """

@add_metadata(inputs=('high', 'low', 'close'))
def calc_trange(high, low, close):
    """True Range"""

    cdef const double[:] high_view = np.asarray(high, float)
    cdef const double[:] low_view = np.asarray(low, float)
    cdef const double[:] close_view = np.asarray(close, float)

    cdef long size = check_size(high_view, low_view, close_view)

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double hi = NAN, lo = NAN, cl = NAN, pc = NAN, tr = NAN

    cdef long i = 0

    with nogil:
        for i in range(size):
            hi, lo, cl, pc = high_view[i], low_view[i], close_view[i], cl

            if not (hi >= lo > 0.0):
                continue

            if pc > hi:
                hi = pc

            if pc < lo:
                lo = pc

            tr = hi - lo

            output[i] = tr

    return result

@add_metadata(inputs=('high', 'low', 'close'))
def calc_atr(high, low, close, long period=14):
    """
    Average True Range

    Args:
        period (int): time period, default 14
    """

    trange = calc_trange(high, low, close)
    result = calc_rma(trange, period)

    return result

@add_metadata(inputs=('high', 'low', 'close'))
def calc_natr(high, low, close, long period=14):
    """
    Normalized Average True Range

    Returns ``100 * ATR(period) / close`` in percentage points.

    Args:
        period (int): time period, default 14
    """

    close = np.asarray(close, float)
    atr = calc_atr(high, low, close, period)

    with np.errstate(divide='ignore', invalid='ignore'):
        result = 100 * atr / close

    return result
