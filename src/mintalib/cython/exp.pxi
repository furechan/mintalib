""" Exponential """

def calc_exp(series):
    """Exponential"""

    cdef const double[:] xs = np.asarray(series, float)

    with np.errstate(invalid='ignore'):
        result = np.exp(xs)

    return result

