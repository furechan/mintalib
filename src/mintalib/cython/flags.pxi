""" Flag functions """


@export
def flag_above(series, double level=0.0, *, double na_value=NAN, bint wrap=True):
    """ returns flag for strictly positive values """

    cdef double[:] xs = np.asarray(series, float)
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


@export
def flag_below(series, double level=0.0, *, double na_value=NAN, bint wrap=True):
    """ returns flag for strictly negative values  """

    cdef double[:] xs = np.asarray(series, float)
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


@export
def invert_flag(series, *, double na_value=NAN, bint wrap=True):
    """ returns flag for strictly negative values  """

    cdef double[:] xs = np.asarray(series, float)
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



@export
def where_flag(flag, x, y, z=NAN, *, bint wrap=True):
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



@export
def updown_flag(series, double up_level=0.0, double down_level=0.0, *,
                double up_flag=1.0, double down_flag=0.0, double start_flag=NAN,
                bint wrap=True):
    """ returns flag according to value crossing up & down levels """

    cdef double[:] xs = np.asarray(series, float)
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

