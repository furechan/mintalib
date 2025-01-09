""" Kaufman Adaptive Moving Average """

def calc_ker(series, int period=10, *, wrap: bool = False):
    """
    Kaufman Efficiency Ratio
    
    Args:
        period (int) : time period, default 10
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x = NAN, px = NAN, dx = NAN
    cdef double y = NAN, py = NAN, dy = NAN

    cdef double erval = NAN, ernum = NAN, erdiv = 0

    cdef long ercnt = 0
    cdef long i = 0, j = 0

    for i in range(size):
        x = xs[i]

        if isnan(x):
            continue

        dx, px = x - px, x

        if isnan(dx):
            continue

        erdiv += math.fabs(dx)
        ercnt += 1

        while ercnt >= period:
            y, j = xs[j], j+1

            if isnan(y):
                continue

            dy, py = y - py, y

            ernum = math.fabs(x-y)
            erval = ernum / erdiv if erdiv else 1.0

            if not isnan(dy):
                erdiv -= math.fabs(dy)
                ercnt -= 1

        output[i] = erval

    if wrap:
        result = wrap_result(result, series)

    return result



def calc_kama(series, int period=10, int fastn=2, int slown=30, *, wrap: bool = False):
    """
    Kaufman Adaptive Moving Average
    
    Args:
        period (int) : time period for efficiency ratio, default 10
        fastn (int) : time period for fast moving average, default, 2
        slown (int) : time period for slow moving average, default 30
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef const double[:] ers = calc_ker(xs, period)

    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double fastf = 2.0 / (fastn + 1.0)
    cdef double slowf = 2.0 / (slown + 1.0)
    cdef double alpha = NAN
    cdef double value = NAN
    cdef double kama = NAN
    cdef double er = NAN

    cdef long i = 0

    for i in range(size):
        value = xs[i]
        er = ers[i]

        if isnan(value) or isnan(er):
            continue

        alpha = (slowf + er * (fastf - slowf)) ** 2.0

        if isnan(kama):
            kama = value
        elif not isnan(alpha):
            kama += alpha * (value - kama)

        output[i] = kama

    if wrap:
        result = wrap_result(result, series)

    return result


