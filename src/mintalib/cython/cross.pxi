""" Cross Over/Under """

def calc_crossover(series, double level=0.0, *, bint wrap=False):
    """
    Cross Over
    
    Yields a value of 1 at the point where series crosses over level

    Args:
        level (float) : level to cross, default 0.0
    """

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


def calc_crossunder(series, double level=0.0, *, wrap: bool = False):
    """
    Cross Under

    Yields a value of 1 at the point where series crosses under level

    Args:
        level (float) : level to cross, default 0.0
    """

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

