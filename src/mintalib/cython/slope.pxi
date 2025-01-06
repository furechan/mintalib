""" Slope (linear regression) """


cdef enum:
    LINREG_SLOPE = 0
    LINREG_INTERCEPT = 1
    LINREG_RVALUE = 2
    LINREG_RSQUARE = 3
    LINREG_RMSERROR = 4
    LINREG_FORECAST = 5
    LINREG_BADOPTION = 6


def linear_regression(series, long period=20, *, int option=0, int offset=0, wrap: bool = False):
    """
    Linear Regression
    
    Args:
        period (int) : time period, default 20
    """

    if option < 0 or option > LINREG_BADOPTION:
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

            if option == LINREG_SLOPE:
                output[j] = slope
            elif option == LINREG_INTERCEPT:
                output[j] = intercept
            elif option == LINREG_RVALUE:
                output[j] = corr
            elif option == LINREG_RSQUARE:
                output[j] = corr * corr
            elif option == LINREG_RMSERROR:
                output[j] = rmse
            elif option == LINREG_FORECAST:
                forecast = intercept + slope * (period + offset -1)
                output[j] = forecast

    if wrap:
        result = wrap_result(result, series)

    return result



def calc_slope(series, long period=20, *, wrap: bool = False):
    """
    Slope (linear regression)
    
    Args:
        period (int) : time period, default 20
    """

    return linear_regression(series, period=period, option=LINREG_SLOPE, wrap=wrap)


def calc_rvalue(series, long period=20, *, wrap: bool = False):
    """
    R-Value (linear regression)
    
    Args:
        period (int) : time period, default 20
    """

    return linear_regression(series, period=period, option=LINREG_RVALUE, wrap=wrap)


def calc_tsf(series, long period=20, long offset=0, *, wrap: bool = False):
    """
    Time Series Forecast (linear regression)
    
    Args:
        period (int) : time period, default 20
    """

    return linear_regression(series, period=period, offset=offset, option=LINREG_FORECAST, wrap=wrap)



@wrap_function(calc_slope)
def SLOPE(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_slope(series, period=period)
    return wrap_result(result, series)


@wrap_function(calc_rvalue)
def RVALUE(series, period: int = 20, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_rvalue(series, period=period)
    return wrap_result(result, series)


@wrap_function(calc_tsf)
def TSF(series, period: int = 20, offset: int = 0, *, item: str = None):
    series = get_series(series, item=item)
    result = calc_tsf(series, period=period, offset=offset)
    return wrap_result(result, series)

