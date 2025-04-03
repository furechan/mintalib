""" Slope (linear regression) """


cdef enum:
    LINREG_SLOPE = 0
    LINREG_INTERCEPT = 1
    LINREG_RVALUE = 2
    LINREG_FORECAST = 4
    LINREG_BADOPTION = 5



def linear_regression(series, long period=20, *, int option=0, int offset=0, bint wrap=False):
    """
    Linear Regression
    
    Args:
        period (int) : time period, default 20
    """

    if period < 2:
        raise ValueError(f"Invalid period {period}, should be greater than 2")  

    if option < 0 or option > LINREG_BADOPTION:
        raise ValueError(f"Invalid option {option}")

    cdef const double[:] ys = np.asarray(series, float)
    cdef long size = ys.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    if period >= size:
        return result

    cdef double x, y
    cdef double s, sx, sy, sxy, sx2, sy2
    cdef double vxy, vxx, vyy
    cdef double corr, slope, intercept, forecast

    cdef long i = 0, j = 0

    s = sx = sy = sxy = sx2 = sy2 = 0.0

    for i in range(size):
        x, y = i, ys[i]

        if y != y:
            s = sx = sy = sxy = sx2 = sy2 = 0.0
            continue

        if s == 0:
            j = i

        s += 1
        sx += x
        sy += y
        sxy += x * y
        sx2 += x * x
        sy2 += y * y

        if s < period:
            continue

        while s > period and j < size:
            x, y, j = j, ys[j], j+1
            s -= 1
            sx -= x
            sy -= y
            sxy -= x * y
            sx2 -= x * x
            sy2 -= y * y

        vxy = (sxy / s - sx * sy / s / s)
        vxx = (sx2 / s - sx * sx / s / s)
        vyy = (sy2 / s - sy * sy / s / s)

        slope = vxy / vxx if vxx > 0  else NAN
        intercept = (sy - slope * sx) / s
        corr = vxy / math.sqrt(vxx * vyy) if vyy > 0 else NAN


        if option == LINREG_SLOPE:
            output[i] = slope
            continue

        if option == LINREG_INTERCEPT:
            output[i] = intercept
            continue

        if option == LINREG_RVALUE:
            output[i] = corr
            continue

        if option == LINREG_FORECAST:
            forecast = intercept + slope * (i + offset)
            output[i] = forecast
            continue

    if wrap:
        result = wrap_result(result, series)

    return result




def calc_slope(series, long period=20, *, bint wrap=False):
    """
    Slope (linear regression)
    
    Args:
        period (int) : time period, default 20
    """

    return linear_regression(series, period=period, option=LINREG_SLOPE, wrap=wrap)


def calc_rvalue(series, long period=20, *, bint wrap=False):
    """
    R-Value (linear regression)
    
    Args:
        period (int) : time period, default 20
    """

    return linear_regression(series, period=period, option=LINREG_RVALUE, wrap=wrap)


def calc_tsf(series, long period=20, long offset=0, *, bint wrap=False):
    """
    Time Series Forecast (linear regression)
    
    Args:
        period (int) : time period, default 20
    """

    return linear_regression(series, period=period, offset=offset, option=LINREG_FORECAST, wrap=wrap)


