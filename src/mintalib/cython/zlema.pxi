""" Zero-Lag Exponential Moving Average """

@add_metadata(same_scale=True)
def calc_zlema(series, long period):
    """
    Zero-Lag Exponential Moving Average

    Args:
        period (int): time period, required

    Formula:
        ZLEMA is an EMA applied to a de-lagged series
        data = 2 * value - value[lag] with lag = (period - 1) // 2
    """

    if period <= 1:
        raise ValueError(f"Invalid period value {period}")

    cdef long lag = (period - 1) // 2

    xs = np.asarray(series, float)
    data = 2 * xs - calc_lag(xs, lag)

    return calc_ema(data, period)
