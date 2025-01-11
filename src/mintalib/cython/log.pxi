""" Logarithm """

def calc_log(series, *, bint wrap=False):
    """ Logarithm """

    cdef const double[:] xs = np.asarray(series, float)

    with np.errstate(invalid='ignore'):
        result = np.log(xs)

    if wrap:
        result = wrap_result(result, series)

    return result

