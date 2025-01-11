""" Moving Average Convergenge Divergence """

macd_result = namedtuple('macd_result', 'macd, macdsignal, macdhist')

def calc_macd(series, long n1=12, long n2=26, long n3=9, *, bint wrap=False):
    """
    Moving Average Convergenge Divergence
    
    Args:
        n1 (int) : show time period, default 12
        n2 (int) : long time periodm, default 26
        n3 (int) : signal time period, default 9  
    
    Outputs:
        macd, macdsignal, macdhist
    """

    ema1 = calc_ema(series, n1)
    ema2 = calc_ema(series, n2)
    macd = ema1 - ema2

    signal = calc_ema(macd, n3)
    hist = macd - signal

    result = macd_result(macd, signal, hist)

    if wrap:
        result = wrap_result(result, series)

    return result

