""" Quadratic Regression """


cdef enum:
    QUADREG_CURVE = 0
    QUADREG_SLOPE = 1
    QUADREG_RVALUE = 2
    QUADREG_RMSE = 3
    QUADREG_FORECAST = 4
    QUADREG_BADOPTION = 5



def quadratic_regression(series, long period=20, *, int option=0, int offset=0):
    """
    Quadratic Regression
    
    Args:
        period (int): time period, default 20
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

    cdef double x, y, xd, yd, xd2
    cdef double s, sx, sx2, sx3, sx4, sy, sy2, sxy, sx2y
    cdef double vxy, vxx, vyy, vxx2, vx2y, vx2x2
    cdef double vzz, vuu, vzu, mse
    cdef double denom, slope, curve, intercept, forecast

    cdef long i = 0

    s = sx = sx2 = sx3 = sx4 = sy = sy2 = sxy = sx2y = 0.0

    with nogil:
        for i in range(size):
            x, y = i, ys[i]

            if y != y:
                s = sx = sx2 = sx3 = sx4 = sy = sy2 = sxy = sx2y = 0.0
                continue

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

            if s > period:
                xd = i - period
                yd = ys[i - period]
                xd2 = xd * xd
                s -= 1
                sx -= xd
                sx2 -= xd2
                sx3 -= xd2 * xd
                sx4 -= xd2 * xd2
                sy -= yd
                sy2 -= yd * yd
                sxy -= xd * yd
                sx2y -= xd2 * yd

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

            if option == QUADREG_SLOPE:
                x = (i + offset)
                output[i] = slope + 2 * curve * x
                continue

            if option == QUADREG_RVALUE:
                # partial correlation of the quadratic term, given the linear term
                vzz = vyy - vxy * vxy / vxx if vxx > 0 else NAN
                vuu = vx2x2 - vxx2 * vxx2 / vxx if vxx > 0 else NAN
                vzu = vx2y - vxy * vxx2 / vxx if vxx > 0 else NAN
                output[i] = vzu / math.sqrt(vzz * vuu) if vzz * vuu > 0 else NAN
                continue

            if option == QUADREG_RMSE:
                mse = vyy - slope * vxy - curve * vx2y
                output[i] = math.sqrt(mse) if mse >= 0 else NAN
                continue

            if option == QUADREG_FORECAST:
                x = (i + offset)
                forecast = intercept + slope * x + curve * x * x
                output[i] = forecast
                continue

    return result



def calc_quadreg(series, long period=20, long offset=0):
    """
    Quadratic Regression (parabolic moving average)

    Value of the regression parabola at the current bar,
    with `offset` projecting the parabola forward.

    Args:
        period (int): time period, default 20
        offset (int): forecast offset, default 0
    """

    return quadratic_regression(series, period=period, offset=offset, option=QUADREG_FORECAST)


def calc_quadreg_curve(series, long period=20):
    """
    Quadratic Regression Curve

    Args:
        period (int): time period, default 20
    """

    return quadratic_regression(series, period=period, option=QUADREG_CURVE)


def calc_quadreg_slope(series, long period=20, long offset=0):
    """
    Quadratic Regression Slope

    Slope of the regression parabola at the current bar,
    with `offset` projecting the slope forward.

    Args:
        period (int): time period, default 20
        offset (int): forecast offset, default 0
    """

    return quadratic_regression(series, period=period, offset=offset, option=QUADREG_SLOPE)


def calc_quadreg_rvalue(series, long period=20):
    """
    Quadratic Regression R-Value

    Partial correlation of the quadratic term, given the linear term.

    Args:
        period (int): time period, default 20
    """

    return quadratic_regression(series, period=period, option=QUADREG_RVALUE)


def calc_quadreg_rmse(series, long period=20):
    """
    Quadratic Regression Root Mean Square Error

    Args:
        period (int): time period, default 20
    """

    return quadratic_regression(series, period=period, option=QUADREG_RMSE)

