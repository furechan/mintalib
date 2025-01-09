""" Rolling Moving Average (RSI Style) """


def calc_rma(series, long period, *, wrap: bool = False):
    """
    Rolling Moving Average (RSI style)

    Exponential moving average with `alpha = 2 / period`,
    that starts as a simple moving average until
    number of bars is equal to `period`.
    """

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double alpha = 1.0 / period
    cdef double value = NAN
    cdef double rma = NAN
    cdef double total = 0.0

    cdef long i = 0, count = 0

    for i in range(size):
        value = xs[i]

        if not isnan(value):
            count += 1
            if count <= period:
                total += value
                rma = total / count
            else:
                rma += alpha * (value - rma)

        if count >= period:
            output[i] = rma

    if wrap:
        result = wrap_result(result, series)

    return result

