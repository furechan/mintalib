""" Flag functions """



def calc_flag(prices, expr: str = None, *, wrap: bool = False):
    """
    Flag Value

    Flag value of 1 for positive, 0 for zero or negative, and NaN for missing values

    Args:
        expr (str) : expression to evaluate (optional) (pandas only!)
    """

    if expr is not None:
        series = calc_eval(prices, expr)
    else:
        series = prices

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value = NAN
    cdef double flag = NAN
    cdef long i = 0

    for i in range(size):
        value = xs[i]

        if isnan(value):
            flag = NAN
        elif value > 0.0:
            flag = 1.0
        else:
            flag = 0.0

        output[i] = flag

    if wrap:
        result = wrap_result(result, series)

    return result


def calc_updown(series, double up_level=0.0, double down_level=0.0, *,
                wrap: bool = False):
    """
    Flag for value crossing up & down levels
    
    Args:
        up_level (float) : flag set at 1 above that level
        down_level (float) : flag set at 0 below that level
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double start_flag=NAN, up_flag = 1.0, down_flag=0.0 
    cdef double value = NAN, prev = NAN
    cdef double flag = start_flag
    cdef long i = 0

    for i in range(size):
        value = xs[i]

        if value > up_level >= prev:
            flag = up_flag
        elif value <= down_level < prev:
            flag = down_flag

        output[i] = flag

        if not isnan(value):
            prev = value

    if wrap:
        result = wrap_result(result, series)

    return result



def where_flag(flag, x, y, z=NAN, *, wrap: bool = False):
    """Value according to flag"""

    cdef const double[:] fs = np.asarray(flag, float)

    cdef long size = fs.size

    cdef const double[:] xs = np.broadcast_to(np.float_(x), size)
    cdef const double[:] ys = np.broadcast_to(np.float_(y), size)
    cdef const double[:] zs = np.broadcast_to(np.float_(z), size)

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value = NAN
    cdef double fval = NAN
    cdef long i = 0

    for i in range(size):
        fval = fs[i]

        if fval > 0:
            value = xs[i]
        elif fval <= 0:
            value = ys[i]
        else:
            value = zs[i]

        output[i] = value

    if wrap:
        result = wrap_result(result, flag)

    return result
