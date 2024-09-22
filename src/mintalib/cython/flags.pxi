""" Flag functions """


def flag_above(series, double level=0.0, *, double na_value=NAN, wrap: bool = False):
    """ Flag for value above level """

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
    """ Flag for value below level """

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



def flag_updown(series, double up_level=0.0, double down_level=0.0, *,
                wrap: bool = False):
    """ Flag for value crossing up & down levels """

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




def flag_invert(series, *, double na_value=NAN, wrap: bool = False):
    """ Inverse flag """

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


def where_flag(flag, x, y, z=NAN, *, wrap: bool = False):
    """ Value according to flag """

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
def FLAG_ABOVE(series, level: float = 0.0, *, item: str = None):
    series = get_series(series, item=item)
    result = flag_above(series, level=level)
    return wrap_result(result, series)


@wrap_function(flag_below)
def FLAG_BELOW(series, level: float = 0.0, *, item: str = None):
    series = get_series(series, item=item)
    result = flag_below(series, level=level)
    return wrap_result(result, series)


@wrap_function(flag_invert)
def FLAG_INVERT(series, *, item: str = None):
    series = get_series(series, item=item)
    result = flag_invert(series)
    return wrap_result(result, series)


@wrap_function(flag_updown)
def FLAG_UPDOWN(series, up_level: float = 0.0, down_level: float = 0.0, *, item: str = None):
    series = get_series(series, item=item)
    result = flag_updown(series, up_level=up_level, down_level=down_level)
    return wrap_result(result, series)

