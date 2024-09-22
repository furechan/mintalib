""" Kaufman Adaptive Moving Average """

def calc_ker(series, int period=10, *, wrap: bool = False):
    """ Kaufman Efficiency Ratio  """

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
    """ Kaufman Adaptive Moving Average """

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



@wrap_function(calc_ker)
def KER(series, period: int = 10, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_ker(series, period=period)
    return wrap_result(result, series)


@wrap_function(calc_kama)
def KAMA(series, period: int = 10, fastn: int = 2, slown: int = 30, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_kama(series, period=period, fastn=fastn, slown=slown)
    return wrap_result(result, series)


