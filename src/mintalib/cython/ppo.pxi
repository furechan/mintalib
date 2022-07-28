""" Moving Average Convergenge Divergence """


@export
def calc_ppo(series, n1=12, n2=26, n3=9):
    """ Price Percentage Oscillator """

    ema1 = calc_ema(series, n1)
    ema2 = calc_ema(series, n2)

    with np.errstate(divide='ignore'):
        ppo = 100 * (ema1 - ema2) / ema2

    signal = calc_ema(ppo, n3)
    hist = ppo - signal
    result = ppo, signal, hist

    if isinstance(series, Series):
        columns = ('ppo', 'pposignal', 'ppohist')
        result = make_dataframe(result, series, columns=columns)

    return result


@export
class PPO(Indicator):
    """ Price Percentage Oscillator """

    def __init__(self, n1=12, n2=26, n3=9, *, item=None):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_ppo(series, self.n1, self.n2, self.n3)
        return result


