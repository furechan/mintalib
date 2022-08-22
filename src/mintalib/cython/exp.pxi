""" Logarithm """


@export
def calc_exp(series):
    """ Exponential """

    cdef double[:] xs = asarray(series, float)

    with np.errstate(invalid='ignore'):
        result = np.log(xs)

    result = wrap_result(result, series)

    return result



class EXP(Indicator):
    """ Exponential """

    same_scale = True

    def __init__(self, period: int, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_exp(series, self.period)
        return result
