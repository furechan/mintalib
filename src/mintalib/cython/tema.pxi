""" Triple Exponential Moving Average """

@add_metadata(same_scale=True)
def calc_tema(series, long period=20):
    """
    Triple Exponential Moving Average

    Args:
        period (int): time period, default 20
    """

    if period <= 0:
        raise ValueError("period must be greater than zero")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size
    if period == 1:
        return np.asarray(xs).copy()

    cdef object result = np.empty(size, float)
    cdef double[:] output = result

    cdef double alpha = 2.0 / (period + 1.0)
    cdef double value = NAN
    cdef double ema1 = NAN, ema2 = NAN, ema3 = NAN
    cdef long i = 0, count1 = 0, count2 = 0, count3 = 0

    with nogil:
        for i in range(size):
            value = xs[i]
            output[i] = NAN

            if isnan(value):
                continue

            count1 += 1
            if isnan(ema1):
                ema1 = value
            else:
                ema1 += alpha * (value - ema1)

            if count1 < period:
                continue

            count2 += 1
            if isnan(ema2):
                ema2 = ema1
            else:
                ema2 += alpha * (ema1 - ema2)

            if count2 < period:
                continue

            count3 += 1
            if isnan(ema3):
                ema3 = ema2
            else:
                ema3 += alpha * (ema2 - ema3)

            if count3 >= period:
                output[i] = 3.0 * ema1 - 3.0 * ema2 + ema3

    return result
