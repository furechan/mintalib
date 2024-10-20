""" Slope (time linear regression) """

cdef enum:
    SLOPE_OPTION_SLOPE = 0
    SLOPE_OPTION_INTERCEPT = 1
    SLOPE_OPTION_RVALUE = 2
    SLOPE_OPTION_RMSERROR = 3
    SLOPE_OPTION_FORECAST = 4

class SlopeOption(IntEnum):
    SLOPE = 0
    INTERCEPT = 1
    RVALUE = 2
    RMSERROR = 3
    FORECAST = 4


def calc_slope(series, long period=20, *, int option=0, int offset=0, wrap: bool = False):
    """
    Slope (time linear regression)
    
    Args:
        period (int) : time period, default 20
    """

    if option < 0 or option > SLOPE_OPTION_FORECAST:
        raise ValueError("Invalid option %d" % option)

    cdef const double[:] ys = np.asarray(series, float)
    cdef long size = ys.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, y, s, sx, sy, sxy, sxx, syy, vxy, vxx, vyy
    cdef double corr, slope, intercept, mse, rmse, forecast

    cdef long i = 0, j = 0

    if period >= size:
        return result

    # 1 <= x <= period
    x = s = sx = sxx = 0.0
    for i in range(period):
        x += 1.0
        s += 1
        sx += x
        sxx += x*x

    vxx = (sxx / s - sx * sx / s / s )

    if vxx <= 0:
        return result

    for j in range(period - 1, size):

        x = 0.0
        sy = sxy = syy = 0.0
        i = j - period + 1

        while i <= j:
            x += 1.0
            y = ys[i]
            if isnan(y):
                break
            sy += y
            sxy += x * y
            syy += y * y
            i += 1
        else:
            vxy = (sxy / s - sx * sy / s / s)
            vyy = (syy / s - sy * sy / s / s)
            slope = vxy / vxx
            intercept = (sy - slope * sx) / s
            corr = vxy / math.sqrt(vxx * vyy) if vyy > 0 else NAN
            mse = vyy * (1 - corr * corr)
            rmse = math.sqrt(mse) if mse >= 0 else NAN

            if option == SLOPE_OPTION_SLOPE:
                output[j] = slope
            elif option == SLOPE_OPTION_INTERCEPT:
                output[j] = intercept
            elif option == SLOPE_OPTION_RVALUE:
                output[j] = corr
            elif option == SLOPE_OPTION_RMSERROR:
                output[j] = rmse
            elif option == SLOPE_OPTION_FORECAST:
                forecast = intercept + slope * (period + offset)
                output[j] = forecast

    if wrap:
        result = wrap_result(result, series)

    return result



@wrap_function(calc_slope)
def SLOPE(series, period: int = 20, *, item: str = None):
    """ Slope (time linear regression) """

    series = get_series(series, item=item)
    result = calc_slope(series, period=period, option=SLOPE_OPTION_SLOPE)
    return wrap_result(result, series)


@wrap_function(calc_slope)
def RVALUE(series, period: int = 20, *, item: str = None):
    """ RValue (time linear regression) """

    series = get_series(series, item=item)
    result = calc_slope(series, period=period, option=SLOPE_OPTION_RVALUE)
    return wrap_result(result, series)


@wrap_function(calc_slope)
def FORECAST(series, period: int = 20, offset: int = 0, *, item: str = None):
    """ Forecast (time linear regression) """

    series = get_series(series, item=item)
    result = calc_slope(series, period=period, offset=offset, option=SLOPE_OPTION_FORECAST)
    return wrap_result(result, series)

