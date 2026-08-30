""" Moving Average Convergence Divergence """

macdv_result = namedtuple('macdv_result', 'macdv, macdvsignal, macdvhist')

@add_metadata(
    output_names=('macdv', 'macdvsignal', 'macdvhist'),
    inputs=('high', 'low', 'close'),
)
def calc_macdv(high, low, close, long n1=12, long n2=26, long n3=9):
    """
    Moving Average Convergence Divergence - Volatility Normalized

    Args:
        n1 (int): short time period, default 12
        n2 (int): long time period, default 26
        n3 (int): signal time period, default 9

    Outputs:
        macdv, macdvsignal, macdvhist
    """

    ema1 = calc_ema(close, n1)
    ema2 = calc_ema(close, n2)
    atr = calc_atr(high, low, close, period=n2)
    macdv = (ema1 - ema2) / atr * 100.0

    signal = calc_ema(macdv, n3)
    hist = macdv - signal

    result = macdv_result(macdv, signal, hist)

    return result
