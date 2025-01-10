""" Logarithm """

def calc_abs(series, *, wrap: bool = False):
    """Absolute Value"""

    cdef const double[:] xs = np.asarray(series, float)

    result = np.abs(xs)

    if wrap:
        result = wrap_result(result, series)

    return result

