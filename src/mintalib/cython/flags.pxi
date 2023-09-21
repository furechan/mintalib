""" Flag functions """



def flag_above(series, double level=0.0, *, double na_value=NAN, wrap: bool = False):
    """ returns flag for strictly positive values """

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
            flag = na_value
        elif value > level:
            flag = 1.0
        else:
            flag = 0.0

        output[i] = flag

    if wrap:
        result = wrap_result(result, series)

    return result



def flag_below(series, double level=0.0, *, double na_value=NAN, wrap: bool = False):
    """ returns flag for strictly negative values  """

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
            flag = na_value
        elif value < level:
            flag = 1.0
        else:
            flag = 0.0

        output[i] = flag

    if wrap:
        result = wrap_result(result, series)

    return result



def invert_flag(series, *, double na_value=NAN, wrap: bool = False):
    """ returns flag for strictly negative values  """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value=NAN
    cdef double flag=NAN
    cdef long i=0

    for i in range(size):
        value = xs[i]

        if isnan(value):
            flag = na_value
        elif value > 0:
            flag = 0.0
        else:
            flag = 1.0

        output[i] = flag

    if wrap:
        result = wrap_result(result, series)

    return result



def updown_flag(series, double up_level=0.0, double down_level=0.0, *,
                double up_flag=1.0, double down_flag=0.0, double start_flag=NAN,
                wrap: bool = False):
    """ returns flag according to value crossing up & down levels """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

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
    """ returns value according to flag """

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



@wrap_function(flag_above)
def FLAG_ABOVE(series, level: float = 0.0, *, na_value: float = NAN, item: str = None):
    series = get_series(series, item=item)
    result = flag_above(series, level=level, na_value=na_value)
    return wrap_result(result, series)


@wrap_function(flag_below)
def FLAG_BELOW(series, level: float = 0.0, *, na_value: float = NAN, item: str = None):
    series = get_series(series, item=item)
    result = flag_below(series, level=level, na_value=na_value)
    return wrap_result(result, series)


@wrap_function(invert_flag)
def INVERT_FLAG(series, *, na_value: float = NAN, item: str = None):
    series = get_series(series, item=item)
    result = invert_flag(series, na_value=na_value)
    return wrap_result(result, series)


@wrap_function(updown_flag)
def UPDOWN_FLAG(series, up_level: float = 0.0, down_level: float = 0.0, *,
                up_flag: float = 1.0, down_flag: float = 0.0, start_flag: float = NAN, item: str = None):
    series = get_series(series, item=item)
    result = updown_flag(series, up_level=up_level, down_level=down_level, up_flag=up_flag, down_flag=down_flag, start_flag=start_flag)
    return wrap_result(result, series)

