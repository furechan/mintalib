""" Price Percentage Oscillator """


ppo_result = namedtuple('ppo_result', 'ppo, pposignal, ppohist')


@export
def calc_ppo(series, long n1=12, long n2=26, long n3=9, wrap: bool = True):
    """ Price Percentage Oscillator """

    ema1 = calc_ema(series, n1, wrap=False)
    ema2 = calc_ema(series, n2, wrap=False)

    with np.errstate(divide='ignore'):
        ppo = 100 * (ema1 - ema2) / ema2

    signal = calc_ema(ppo, n3, wrap=False)
    hist = ppo - signal

    result = ppo_result(ppo, signal, hist)

    if wrap:
        result = wrap_result(result, series)

    return result


class PPO(Indicator):
    """ Price Percentage Oscillator """

    def __init__(self, n1: int = 12, n2: int =26, n3: int =9, *, item=None):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_ppo(series, self.n1, self.n2, self.n3, wrap=True)
        return result


