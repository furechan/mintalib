""" Zero-Lag Exponential Moving Average """

@add_metadata(same_scale=True)
def calc_zlema(series, long period):
    """
    Zero-Lag Exponential Moving Average

    Args:
        period (int): time period, required

    Formula:
        ZLEMA is an EMA applied to a de-lagged series
        data = 2 * value - value[lag] with lag = (period - 1) // 2
    """

    if period <= 0:
        raise ValueError("period must be greater than zero")
    # Graceful degradation: a one-period moving average is the input itself.
    if period == 1:
        return np.asarray(series, float).copy()

    cdef long lag = (period - 1) // 2
    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.empty(size, float)
    cdef double[:] output = result

    cdef double alpha = 2.0 / (period + 1.0)
    cdef double value = NAN, lagged = NAN, adjusted = NAN, ema = NAN
    cdef long i = 0, count = 0

    with nogil:
        for i in range(size):
            output[i] = NAN

            if i < lag:
                continue

            value = xs[i]
            lagged = xs[i - lag]
            if isnan(value) or isnan(lagged):
                continue

            adjusted = 2.0 * value - lagged
            count += 1

            if isnan(ema):
                ema = adjusted
            else:
                ema += alpha * (adjusted - ema)

            if count >= period:
                output[i] = ema

    return result
