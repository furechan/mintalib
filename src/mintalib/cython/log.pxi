""" Logarithm """


def calc_log(series, *, wrap: bool = False):
    """ Logarithm """

    cdef const double[:] xs = np.asarray(series, float)

    with np.errstate(invalid='ignore'):
        result = np.log(xs)

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_function(calc_log)
def LOG(series, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_log(series)
    return wrap_result(result, series)

