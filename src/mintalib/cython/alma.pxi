"""Arnaud Legoux Moving Average"""


def calc_alma(series, long period = 9, double offset = 0.85, double sigma = 6.0, *, wrap: bool = False):
    """Arnaud Legoux Moving Average"""
    m = offset * (period - 1)
    s = period / sigma
    w = np.array([np.exp(-((i - m) ** 2) / (2 * s**2)) for i in range(period)])
    w = w / w.sum()

    padding = np.full(period-1, np.nan)
    result = np.correlate(series, w, "valid")
    result = np.insert(result, 0, padding)

    if wrap:
        result = wrap_result(result, series)

    return result
