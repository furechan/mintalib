""" Exponential Moving Average """



@export
def calc_ema(series, long period, *, bint adjust = False, wrap: bool = True):
    """
    Exponential Moving Average

    Args:
        series (series) : data series, required
        period (int) : time period, required
        adjust (bool) : whether to adjust weights, default False
            when true update ratio increases gradually (see formula)

    Formula:
        EMA is calculated as a recursive formula
        The standard formula is ema += alpha * (value - ema)
            with alpha = 2.0 / (period + 1.0)
        The adjusted formula is ema = num/div
            where num = value + rho * num, div = 1.0 + rho * div
            with rho = 1.0 - alpha
    """

    if period <= 1:
        raise ValueError(f"Invalid period value {period}")

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double alpha = 2.0 / (period + 1.0)
    cdef double rho = (1.0 - alpha)
    cdef double value = NAN
    cdef double num = NAN, div=NAN
    cdef double ema = NAN

    cdef long i = 0, count = 0

    for i in range(size):
        value = xs[i]

        if not isnan(value):
            count += 1

            if isnan(ema):
                ema = value
                num = value
                div = 1.0
            elif adjust:
                num = value + rho * num
                div = 1.0 + rho * div
                ema = num / div
            else:
                ema += alpha * (value - ema)

        if count >= period:
            output[i] = ema

    if wrap:
        result = wrap_result(result, series)

    return result


@wrap_indicator(calc_ema)
class EMA(Indicator):

    same_scale = True

    def __init__(self, period: int, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_ema(series, self.period, wrap=True)
        return result
