""" Average Directional Index """

dmi_result = namedtuple('dmi_result', 'adx, pdi, mdi')

@add_metadata(output_names=('adx', 'pdi', 'mdi'))
def calc_dmi(prices, long period=14):
    """
    Directional Movement Indicator

    Args:
        period (int) : time period, default 14
    """

    high = np.asarray(prices['high'], float)
    low = np.asarray(prices['low'], float)

    atr = calc_atr(prices, period)
    hm = calc_diff(high, 1)
    lm = -calc_diff(low, 1)

    pdm = np.where((hm > lm) & (hm > 0), hm, 0)
    mdm = np.where((lm > hm) & (lm > 0), lm, 0)

    with np.errstate(divide='ignore'):
        pdi = 100 * calc_rma(pdm, period) / atr
        mdi = 100 * calc_rma(mdm, period) / atr
        dx = 100 * np.abs(pdi - mdi) / (pdi + mdi)

    adx = calc_rma(dx, period)

    result = dmi_result(adx, pdi, mdi)

    return result


def calc_adx(prices, long period=14):
    """
    Average Directional Index

    Args:
        period (int) : time period, default 14
    """

    result = calc_dmi(prices, period=period).adx

    return result


def calc_pdi(prices, long period=14):
    """
    Plus Directional Index

    Args:
        period (int) : time period, default 14
    """

    result = calc_dmi(prices, period=period).pdi

    return result


def calc_mdi(prices, long period=14):
    """
    Minus Directional Index

    Args:
        period (int) : time period, default 14
    """

    result = calc_dmi(prices, period=period).mdi

    return result

