""" Logarithm """

def calc_log(series):
    """ Logarithm """

    cdef const double[:] xs = np.asarray(series, float)

    with np.errstate(invalid='ignore'):
        result = np.log(xs)

    return result

