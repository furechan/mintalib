""" exponential moving average """




def calc_rma(series, long period=14):
    """
    RSI style Moving Average

    Args:
        series (series) : The input series. Required
        period (int) : The indicator period. Default 14

    Returns:
        A series
    """

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double alpha = 1.0 / period
    cdef double value = NAN
    cdef double rma = NAN
    cdef double sum = 0.0

    cdef long i = 0, count = 0

    for i in range(size):
        value = xs[i]

        if not isnan(value):
            count += 1

            if count <= period:
                sum += value
                rma = sum / count
            else:
                rma += alpha * (value - rma)

        if count >= period:
            output[i] = rma

    if isinstance(series, Series):
        result = make_series(result, series)

    return result



@export
class RMA(Indicator):
    """ RSI Style Moving Average"""

    same_scale = True

    def __init__(self, period=14, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_rma(series, self.period)
        return result
