""" Logarithm """

def calc_abs(series):
    """Absolute Value"""

    cdef const double[:] xs = np.asarray(series, float)

    result = np.abs(xs)

    return result

