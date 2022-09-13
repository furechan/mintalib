""" Cross Over/Under """


@export
def crossover(series, double level=0.0, bint wrap=True):
    """ 1 when data cross over level, 0.0 elsewhere """

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, 0, dtype=int)
    cdef int[:] output = result

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


@export
def crossunder(series, double level=0.0, bint wrap=True):
    """ 1 when data cross under level, 0.0 elsewhere """

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, 0, dtype=int)
    cdef int[:] output = result

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

