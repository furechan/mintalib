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

    cdef const double[:] zs = np.asarray(series, float)
    cdef long size = zs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    if period >= size:
        return result

    # windows reset on nan, so every emitted window is a contiguous integer
    # grid - the pure-x moments on the centered grid u = x - xbar are the
    # same for every window and can be precomputed
    cdef double s = 0.0, su2 = 0.0, su4 = 0.0
    cdef double u = (1 - period) / 2.0
    cdef long k = 0

    for k in range(period):
        s += 1
        su2 += u * u
        su4 += u * u * u * u
        u += 1.0

    cdef double vxx = su2 / s
    cdef double vuu = su4 / s - su2 * su2 / s / s

    if vxx <= 0 or vuu <= 0:
        return result

    # anchored one-pass rolling sums; max_x trades rewind overhead
    # against precision in the anchored x sums
    cdef double max_x = 1000.0 if period < 500 else 2.0 * period
    cdef double half = (period - 1) / 2.0

    cdef double x, z, xj, zj, xbar, x_end
    cdef double sz, sxz, sx2z, szz
    cdef double suz, su2z, szz_r
    cdef double vuz, vzz
    cdef double slope, curve, rvalue, alpha, mse

    cdef long i = 0, j = 0, nexti = 0, anchor = 0, c = 0

    sz = sxz = sx2z = szz = 0.0

    with nogil:
        while nexti < size:
            i = nexti
            nexti += 1
            x = i - anchor
            z = zs[i]

            if z != z or x > max_x:
                if x > max_x:  # rewind: replay from the window back with a fresh anchor
                    nexti = j
                c = 0
                sz = sxz = sx2z = szz = 0.0
                anchor = nexti
                continue

            if c == 0:
                j = i

            c += 1
            sz += z
            sxz += x * z
            sx2z += x * x * z
            szz += z * z

            while c > period:
                xj = j - anchor
                zj = zs[j]
                j += 1
                c -= 1
                sz -= zj
                sxz -= xj * zj
                sx2z -= xj * xj * zj
                szz -= zj * zj

            if c < period:
                continue

            # shift the raw sums to the centered grid (where su = su3 = 0)
            xbar = x - half
            suz = sxz - xbar * sz
            su2z = sx2z - 2.0 * xbar * sxz + xbar * xbar * sz

            slope = suz / s / vxx

            # residuals z' = z - slope*u: sum of z' equals sz and sum of u^2*z' equals su2z
            szz_r = szz - 2.0 * slope * suz + slope * slope * su2

            vuz = su2z / s - su2 * sz / s / s
            vzz = szz_r / s - sz * sz / s / s

            curve = vuz / vuu
            rvalue = vuz / math.sqrt(vuu * vzz) if vuu * vzz > 0 else NAN


            if option == QUADREG_CURVE:
                output[i] = curve
                continue

            if option == QUADREG_SLOPE:
                # tangent slope of the parabola at the current bar (u = half)
                x_end = half + offset
                output[i] = slope + 2 * curve * x_end
                continue

            if option == QUADREG_RVALUE:
                # partial correlation of the quadratic term, given the linear term
                output[i] = rvalue
                continue

            if option == QUADREG_RMSE:
                mse = (1 - rvalue * rvalue) * vzz
                output[i] = math.sqrt(mse) if mse >= 0 else NAN
                continue

            if option == QUADREG_FORECAST:
                # centered u makes u and u^2 orthogonal, so the stage-1 slope is
                # the full-model coefficient and the residual sum of z' equals sz
                alpha = sz / s - curve * su2 / s
                x_end = half + offset
                output[i] = alpha + slope * x_end + curve * x_end * x_end
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
