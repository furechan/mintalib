""" Average Directional Index """

dmi_result = namedtuple('dmi_result', 'adx, pdi, mdi')

cdef tuple _calc_di(high, low, close, long period, bint want_pdi, bint want_mdi):
    """Calculate one or both directional indexes without calculating ADX."""
    high = np.asarray(high, float)
    low = np.asarray(low, float)
    close = np.asarray(close, float)

    cdef long size = check_size(high, low, close)

    atr = calc_atr(high, low, close, period)
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

@add_metadata(
    output_names=('adx', 'pdi', 'mdi'),
    inputs=('high', 'low', 'close'),
)
def calc_dmi(high, low, close, long period=14):
    """
    Directional Movement Indicator

    Args:
        period (int): time period, default 14
    """

    pdi, mdi = _calc_di(high, low, close, period, True, True)

    with np.errstate(divide='ignore'):
        dx = 100 * np.abs(pdi - mdi) / (pdi + mdi)

    adx = calc_rma(dx, period)

    result = dmi_result(adx, pdi, mdi)

    return result

@add_metadata(inputs=('high', 'low', 'close'))
def calc_adx(high, low, close, long period=14):
    """
    Average Directional Index

    Args:
        period (int): time period, default 14
    """

    pdi, mdi = _calc_di(high, low, close, period, True, True)

    with np.errstate(divide='ignore'):
        dx = 100 * np.abs(pdi - mdi) / (pdi + mdi)

    return calc_rma(dx, period)

@add_metadata(inputs=('high', 'low', 'close'))
def calc_pdi(high, low, close, long period=14):
    """
    Plus Directional Index

    Args:
        period (int): time period, default 14
    """

    pdi, _ = _calc_di(high, low, close, period, True, False)
    return pdi

@add_metadata(inputs=('high', 'low', 'close'))
def calc_mdi(high, low, close, long period=14):
    """
    Minus Directional Index

    Args:
        period (int): time period, default 14
    """

    _, mdi = _calc_di(high, low, close, period, False, True)
    return mdi
