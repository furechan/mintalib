""" Curve (quadratic regression) """


cdef enum:
    QUADREG_CURVE = 0
    QUADREG_FORECAST = 1
    QUADREG_BADOPTION = 2



def quadratic_regression(series, long period=20, *, int option=0, int offset=0, bint wrap=False):
    """
    Quadratic Regression
    
    Args:
        period (int) : time period, default 20
    """


    if period < 2:
        raise ValueError(f"Invalid period {period}, should be greater than 2")  

    if option < 0 or option > QUADREG_BADOPTION:
        raise ValueError(f"Invalid option {option}")

    cdef const double[:] ys = np.asarray(series, float)
    cdef long size = ys.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    if period >= size:
        return result

    cdef double x, y
    cdef double s, sx, sx2, sx3, sx4, sy, sy2, sxy, sx2y
    cdef double vxy, vxx, vyy, vxx2, vx2y, vx2x2
    cdef double denom, slope, curve, intercept, forecast

    cdef long i = 0, j = 0

    s = sx = sx2 = sx3 = sx4 = sy = sy2 = sxy = sx2y = 0.0

    for i in range(size):
        x, y = i, ys[i]

        if y != y:
            s = sx = sx2 = sx3 = sx4 = sy = sy2 = sxy = sx2y = 0.0
            continue

        if s == 0:
            j = i

        s += 1
        sx += x
        sx2 += x * x
        sx3 += x * x * x
        sx4 += x * x * x * x
        sy += y
        sy2 += y * y
        sxy += x * y
        sx2y += x * x * y

        if s < period:
            continue

        while s > period and j < size:
            x, y, j = j, ys[j], j+1
            s -= 1
            sx -= x
            sx2 -= x * x
            sx3 -= x * x * x
            sx4 -= x * x * x * x
            sy -= y
            sy2 -= y * y
            sxy -= x * y
            sx2y -= x * x * y

        vxy = (sxy / s - sx * sy / s / s)
        vxx = (sx2 / s - sx * sx / s / s)
        vyy = (sy2 / s - sy * sy / s / s)
        vxx2 = (sx3 / s - sx * sx2 / s / s)
        vx2y = (sx2y / s - sx2 * sy / s / s)
        vx2x2 = (sx4 / s - sx2 * sx2 / s / s)

        denom = vx2x2 * vxx - vxx2 * vxx2
        curve = (vx2y * vxx - vxy * vxx2) / denom if denom > 0 else NAN
        slope = (vxy * vx2x2 - vxx2 * vx2y) / denom if denom > 0 else NAN
        intercept = (sy - slope * sx - curve * sx2) / s if s > 0 else NAN


        if option == QUADREG_CURVE:
            output[i] = curve
            continue

        if option == QUADREG_FORECAST:
            x = (i + offset)
            forecast = intercept + slope * x + curve * x * x
            output[i] = forecast
            continue

    if wrap:
        result = wrap_result(result, series)

    return result



def calc_curve(series, long period=20, *, bint wrap=False):
    """ Curve (quadratic regression) """

    return quadratic_regression(series, period=period, option=QUADREG_CURVE, wrap=wrap)


def calc_qsf(series, long period=20, long offset=0, *, bint wrap=False):
    """
    Quadratic Series Forecast (quadratic regression)
    
    Args:
        period (int) : time period, default 20
    """

    return quadratic_regression(series, period=period, offset=offset, option=QUADREG_FORECAST, wrap=wrap)
