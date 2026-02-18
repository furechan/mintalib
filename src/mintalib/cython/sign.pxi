""" Sign function """


def calc_sign(series):
    """Sign"""

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value = NAN
    cdef double sign = NAN
    cdef long i = 0

    for i in range(size):
        value = xs[i]

        if value > 0:
            sign = 1.0
        elif value < 0:
            sign = -1.0
        elif value == 0:
            sign = 0.0

        output[i] = sign

    return result


