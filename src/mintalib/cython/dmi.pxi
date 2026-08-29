""" Average Directional Index """

dmi_result = namedtuple('dmi_result', 'adx, pdi, mdi')


cdef tuple _calc_di(prices, long period, bint want_pdi, bint want_mdi):
    """Calculate one or both directional indexes without calculating ADX."""
    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)

    atr = calc_atr(prices, period)
    hm = calc_diff(high, 1)
    lm = -calc_diff(low, 1)

    pdi = None
    mdi = None

    with np.errstate(divide='ignore'):
        if want_pdi:
            pdm = np.where((hm > lm) & (hm > 0), hm, 0)
            pdi = 100 * calc_rma(pdm, period) / atr
        if want_mdi:
            mdm = np.where((lm > hm) & (lm > 0), lm, 0)
            mdi = 100 * calc_rma(mdm, period) / atr

    return pdi, mdi


@add_metadata(output_names=('adx', 'pdi', 'mdi'))
def calc_dmi(prices, long period=14):
    """
    Directional Movement Indicator

    Args:
        period (int): time period, default 14
    """

    pdi, mdi = _calc_di(prices, period, True, True)

    with np.errstate(divide='ignore'):
        dx = 100 * np.abs(pdi - mdi) / (pdi + mdi)

    adx = calc_rma(dx, period)

    result = dmi_result(adx, pdi, mdi)

    return result


def calc_adx(prices, long period=14):
    """
    Average Directional Index

    Args:
        period (int): time period, default 14
    """

    pdi, mdi = _calc_di(prices, period, True, True)

    with np.errstate(divide='ignore'):
        dx = 100 * np.abs(pdi - mdi) / (pdi + mdi)

    return calc_rma(dx, period)


def calc_pdi(prices, long period=14):
    """
    Plus Directional Index

    Args:
        period (int): time period, default 14
    """

    pdi, _ = _calc_di(prices, period, True, False)
    return pdi


def calc_mdi(prices, long period=14):
    """
    Minus Directional Index

    Args:
        period (int): time period, default 14
    """

    _, mdi = _calc_di(prices, period, False, True)
    return mdi
