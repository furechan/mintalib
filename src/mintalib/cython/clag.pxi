""" Confirmation Lag """

@with_metadata(same_scale=True)
def calc_clag(series, long period=1, *, bint wrap=False):
    """
    Confirmation Lag

    Changes value only after a confirmation period 

    Args:
        period (int) : time period, default 1
    """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")


    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value = NAN, prev = NAN, clag = NAN

    cdef long i = 0, count = 0

    for i in range(size):
        value = xs[i]

        if isnan(value):
            continue

        if prev != value:
            prev = value
            count = 0
        else:
            count += 1

        if count >= period:
            clag = value

        output[i] = clag

    if wrap:
        result = wrap_result(result, series)

    return result



