""" Moving Average Convergenge Divergence """


@export
def calc_macd(series, n1=12, n2=26, n3=9):
    """ Moving Average Convergenge Divergence """

    ema1 = calc_ema(series, n1)
    ema2 = calc_ema(series, n2)

    macd = ema1 - ema2
    signal = calc_ema(macd, n3)
    hist = macd - signal
    result = macd, signal, hist

    if isinstance(series, Series):
        columns = ('macd', 'macdsignal', 'macdhist')
        result = make_dataframe(result, series, columns=columns)

    return result


@export
class MACD(Indicator):
    """ Moving Average Convergence Divergence """

    def __init__(self, n1=12, n2=26, n3=9, *, item=None):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_macd(series, self.n1, self.n2, self.n3)
        return result


