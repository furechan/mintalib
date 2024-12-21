""" Average Directional Index """

dmi_result = namedtuple('dmi_result', 'adx, pdi, mdi')


def calc_dmi(prices, long period=14, *, wrap: bool = False):
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

    if wrap:
        result = wrap_result(result, prices)

    return result


def calc_adx(prices, long period=14, *, wrap: bool = False):
    """
    Average Directional Index

    Args:
        period (int) : time period, default 14
    """

    result = calc_dmi(prices, period=period).adx

    if wrap:
        result = wrap_result(result, prices)

    return result


def calc_pdi(prices, long period=14, *, wrap: bool = False):
    """
    Plus Directional Index

    Args:
        period (int) : time period, default 14
    """

    result = calc_dmi(prices, period=period).pdi

    if wrap:
        result = wrap_result(result, prices)

    return result


def calc_mdi(prices, long period=14, *, wrap: bool = False):
    """
    Minus Directional Index

    Args:
        period (int) : time period, default 14
    """

    result = calc_dmi(prices, period=period).mdi

    if wrap:
        result = wrap_result(result, prices)

    return result


@wrap_function(calc_dmi)
def DMI(prices, period: int = 14):
    result = calc_dmi(prices, period=period)
    return wrap_result(result, prices)


@wrap_function(calc_adx)
def ADX(prices, period: int = 14):
    result = calc_adx(prices, period=period)
    return wrap_result(result, prices)


@wrap_function(calc_pdi)
def PDI(prices, period: int = 14):
    result = calc_pdi(prices, period=period)
    return wrap_result(result, prices)


@wrap_function(calc_mdi)
def MDI(prices, period: int = 14):
    result = calc_mdi(prices, period=period)
    return wrap_result(result, prices)

