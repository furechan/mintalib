""" Moving Average Convergenge Divergence """

macdv_result = namedtuple('macdv_result', 'macdv, macdvsignal, macdvhist')

@add_metadata(output_names=('macdv', 'macdvsignal', 'macdvhist'))
def calc_macdv(prices, long n1=12, long n2=26, long n3=9):
    """
    Moving Average Convergenge Divergence - Volatility Normalized
    
    Args:
        n1 (int) : show time period, default 12
        n2 (int) : long time periodm, default 26
        n3 (int) : signal time period, default 9  
    
    Outputs:
        macdv, macdvsignal, macdvhist
    """

    close = prices['close']

    ema1 = calc_ema(close, n1)
    ema2 = calc_ema(close, n2)
    atr = calc_atr(prices, period=n2)
    macdv = (ema1 - ema2) / atr * 100.0

    signal = calc_ema(macdv, n3)
    hist = macdv - signal

    result = macdv_result(macdv, signal, hist)

    return result

