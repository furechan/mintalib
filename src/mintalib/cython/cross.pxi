""" Cross Over/Under """

def crossover(series, double level=0.0, *, wrap: bool = False):
    """ Cross Over """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, 0, dtype=float)
    cdef double[:] output = result

    cdef double prev = NAN, value = NAN

    cdef long i = 0

    for i in range(size):
        value = xs[i]

        if value > level >= prev:
            output[i] = 1

        if not isnan(value):
            prev = value

    if wrap:
        result = wrap_result(result, series)

    return result


def crossunder(series, double level=0.0, *, wrap: bool = False):
    """ Cross Under """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, 0, dtype=float)
    cdef double[:] output = result

    cdef double prev = NAN, value = NAN
    cdef long i = 0

    for i in range(size):
        value = xs[i]

        if value < level <= prev:
            output[i] = 1

        if not isnan(value):
            prev = value

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(crossover)
def CROSSOVER(series, level: float = 0.0, *, item: str = None):
    series = get_series(series, item=item)
    result = crossover(series, level=level)
    return wrap_result(result, series)


@wrap_function(crossunder)
def CROSSUNDER(series, level: float = 0.0, *, item: str = None):
    series = get_series(series, item=item)
    result = crossunder(series, level=level)
    return wrap_result(result, series)
