""" Linear Regression """


cdef enum:
    LINREG_SLOPE = 0
    LINREG_INTERCEPT = 1
    LINREG_RVALUE = 2
    LINREG_RMSE = 3
    LINREG_FORECAST = 4
    LINREG_BADOPTION = 5



def linear_regression(series, long period=20, *, int option=0, int offset=0):
    """
    Linear Regression
    
    Args:
        period (int): time period, default 20
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
    cdef double corr, slope, intercept, forecast, mse

    cdef long i = 0, j = 0

    s = sx = sy = sxy = sx2 = sy2 = 0.0

    with nogil:
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

            if option == LINREG_RMSE:
                mse = vyy * (1 - corr * corr)
                output[i] = math.sqrt(mse) if mse >= 0 else NAN
                continue

            if option == LINREG_FORECAST:
                forecast = intercept + slope * (i + offset)
                output[i] = forecast
                continue

    return result



def calc_linreg(series, long period=20, long offset=0):
    """
    Linear Regression (least squares moving average)

    Value of the regression line at the current bar,
    with `offset` projecting the line forward.

    Args:
        period (int): time period, default 20
        offset (int): forecast offset, default 0
    """

    return linear_regression(series, period=period, offset=offset, option=LINREG_FORECAST)



def calc_linreg_slope(series, long period=20):
    """
    Linear Regression Slope

    Args:
        period (int): time period, default 20
    """

    return linear_regression(series, period=period, option=LINREG_SLOPE)


def calc_linreg_rvalue(series, long period=20):
    """
    Linear Regression R-Value

    Args:
        period (int): time period, default 20
    """

    return linear_regression(series, period=period, option=LINREG_RVALUE)


def calc_linreg_rmse(series, long period=20):
    """
    Linear Regression Root Mean Square Error

    Args:
        period (int): time period, default 20
    """

    return linear_regression(series, period=period, option=LINREG_RMSE)

