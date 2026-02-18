""" Rolling Mean Absolute Deviation """


def calc_mad(series, period: int = 14):
    """Rolling Mean Absolute Deviation"""

    if period <= 0:
        raise ValueError(f"Invalid period value {period}")

    cdef const double[:] xs = np.asarray(series, float)

    diff = xs - calc_sma(xs, period)
    result = calc_sma(np.abs(diff), period)

    return result
