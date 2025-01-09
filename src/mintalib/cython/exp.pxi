""" Exponential """

def calc_exp(series, *, wrap: bool = False):
    """Exponential"""

    cdef const double[:] xs = np.asarray(series, float)

    with np.errstate(invalid='ignore'):
        result = np.exp(xs)

    if wrap:
        result = wrap_result(result, series)

    return result

