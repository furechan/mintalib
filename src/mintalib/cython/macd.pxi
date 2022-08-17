""" Moving Average Convergenge Divergence """


@export
def calc_macd(series, long n1=12, long n2=26, long n3=9):
    """ Moving Average Convergenge Divergence """

    ema1 = calc_ema(series, n1, wrap=False)
    ema2 = calc_ema(series, n2, wrap=False)

    macd = ema1 - ema2
    signal = calc_ema(macd, n3, wrap=False)
    hist = macd - signal

    result = dict(
        macd=macd,
        macdsignal=signal,
        macdhist=hist
    )

    result = wrap_result(result, series)

    return result


class MACD(Indicator):
    """ Moving Average Convergence Divergence """

    def __init__(self, n1: int = 12, n2: int = 26, n3: int = 9, *, item=None):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_macd(series, self.n1, self.n2, self.n3)
        return result


