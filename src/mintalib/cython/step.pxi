""" Step Function """


def calc_step(series, threshold : float = 1.0):
    """
    Step Function

    Limit value changes to threshold (in absolute value)

    Args:
        threshold (float) : threshold value, default 1.0
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value = NAN, prev = NAN
    cdef double ul = NAN, ll=NAN

    cdef long i = 0

    for i in range(size):
        value, prev = xs[i], value

        if isnan(value) or isnan(prev):
            continue

        ul, ll = prev + threshold, prev - threshold

        if value > ul:
            value = ul
        elif value < ll:
            value = ll

        output[i] = value

    return result



