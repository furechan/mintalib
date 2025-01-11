""" Price Percentage Oscillator """

ppo_result = namedtuple('ppo_result', 'ppo, pposignal, ppohist')

def calc_ppo(series, long n1=12, long n2=26, long n3=9, *, bint wrap=False):
    """
    Price Percentage Oscillator
    
    Args:
        n1 (int) : short time period, default 12
        n2 (int) : long time period, default 26
        n3 (int) : signal time period, default 9

    Outputs:
        ppo, pposignal, ppohist
    """

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



