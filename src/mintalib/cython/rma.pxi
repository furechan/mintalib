""" Rolling Moving Average (RSI Style) """




def calc_rma(series, long period=14):
    """
    Rolling Moving Average (RSI Style)

    Args:
        series (series) : data series. required
        period (int) : time period. default 14
    """

    cdef double[:] xs = asarray(series, float)
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

    result = wrap_result(result, series)

    return result



@export
class RMA(Indicator):
    """
    Rolling Moving Average (RSI Style)

    Args:
        period (int) : time period. default 14
    """

    same_scale = True

    def __init__(self, period : int = 14, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_rma(series, self.period)
        return result
