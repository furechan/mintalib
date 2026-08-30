""" Relative Strength Index """

def calc_rsi(series, long period=14):
    """
    Relative Strength Index

    Args:
        period (int): time period, default 14
    """

    if period <= 0:
        raise ValueError("period must be greater than zero")

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value = NAN, previous = NAN, change = NAN
    cdef double gain = 0.0, loss = 0.0
    cdef double avg_gain = 0.0, avg_loss = 0.0, total = 0.0
    cdef double alpha = 1.0 / period
    cdef long i = 0, count = 0

    with nogil:
        for i in range(size):
            value = xs[i]
            if isnan(value):
                continue
            if isnan(previous):
                previous = value
                continue

            change = value - previous
            previous = value
            gain = change if change > 0.0 else 0.0
            loss = -change if change < 0.0 else 0.0
            count += 1

            if count <= period:
                avg_gain += gain
                avg_loss += loss
                if count < period:
                    continue
                avg_gain /= period
                avg_loss /= period
            else:
                avg_gain += alpha * (gain - avg_gain)
                avg_loss += alpha * (loss - avg_loss)

            total = avg_gain + avg_loss
            output[i] = 100.0 * avg_gain / total if total > 0.0 else 0.0

    return result
