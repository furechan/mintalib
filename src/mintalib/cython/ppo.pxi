""" Price Percentage Oscillator """


ppo_result = namedtuple('ppo_result', 'ppo, pposignal, ppohist')


def calc_ppo(series, long n1=12, long n2=26, long n3=9, *, wrap: bool = False):
    """ Price Percentage Oscillator """

    ema1 = calc_ema(series, n1)
    ema2 = calc_ema(series, n2)

    with np.errstate(divide='ignore'):
        ppo = 100 * (ema1 - ema2) / ema2

    signal = calc_ema(ppo, n3)
    hist = ppo - signal

    result = ppo_result(ppo, signal, hist)

    if wrap:
        result = wrap_result(result, series)

    return result



@wrap_function(calc_ppo)
def PPO(series, n1: int = 12, n2: int = 26, n3: int = 9, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_ppo(series, n1=n1, n2=n2, n3=n3)
    return wrap_result(result, series)

