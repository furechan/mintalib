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

    # windows reset on nan, so every emitted window is a contiguous integer
    # grid - the pure-x moments on the 1..period grid are the same for every
    # window and can be precomputed
    cdef double x = 0.0, s = 0.0, sx = 0.0, sxx = 0.0
    cdef long k = 0

    for k in range(period):
        x += 1.0
        s += 1
        sx += x
        sxx += x * x

    cdef double vxx = sxx / s - sx * sx / s / s

    if vxx <= 0:
        return result

    # anchored one-pass rolling sums; max_x trades rewind overhead
    # against precision in the anchored x sums
    cdef double max_x = 1000.0 if period < 500 else 2.0 * period

    cdef double xa, y, xj, yj
    cdef double sy, sxy, syy, sxy_g
    cdef double vxy, vyy
    cdef double corr, slope, intercept, mse

    cdef long i = 0, j = 0, nexti = 0, anchor = 0, c = 0

    sy = sxy = syy = 0.0

    with nogil:
        while nexti < size:
            i = nexti
            nexti += 1
            xa = i - anchor
            y = ys[i]

            if y != y or xa > max_x:
                if xa > max_x:  # rewind: replay from the window back with a fresh anchor
                    nexti = j
                c = 0
                sy = sxy = syy = 0.0
                anchor = nexti
                continue

            if c == 0:
                j = i

            c += 1
            sy += y
            sxy += xa * y
            syy += y * y

            while c > period:
                xj = j - anchor
                yj = ys[j]
                j += 1
                c -= 1
                sy -= yj
                sxy -= xj * yj
                syy -= yj * yj

            if c < period:
                continue

            # shift the anchored sum of x*y onto the 1..period grid the constants use
            sxy_g = sxy + (period - xa) * sy

            vxy = sxy_g / s - sx * sy / s / s
            vyy = syy / s - sy * sy / s / s

            slope = vxy / vxx
            intercept = (sy - slope * sx) / s
            corr = vxy / math.sqrt(vxx * vyy) if vyy > 0 else NAN


            if option == LINREG_SLOPE:
                output[i] = slope
                continue

            if option == LINREG_INTERCEPT:
                # fitted value at x=0, one bar before the window
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
                # the current bar sits at x=period on the grid
                output[i] = intercept + slope * (period + offset)
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
