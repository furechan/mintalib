""" Curve (quadratic regression) """


cdef enum:
    QUADREG_SLOPE = 0
    QUADREG_CURVE = 1
    QUADREG_RVALUE = 2
    QUADREG_RSQUARE = 3
    QUADREG_RMSERROR = 4
    QUADREG_BADOPTION = 5



def quadratic_regression(series, long period=20, *, int option=0, bint wrap=False):
    """ Curve (quadratic regression) """

    if option < 0 or option >= QUADREG_BADOPTION:
        raise ValueError("Invalid option %d" % option)

    cdef const double[:] zs = np.asarray(series, float)
    cdef long size = zs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, sx, sxx, vxx
    cdef double y, sy, syy, vyy
    cdef double z, sz, szz, vzz
    cdef double s, sxz, vxz, syz, vyz

    cdef double slope, curve, intercept, mse, rmse, rvalue, rsquare

    cdef bint skip = 0

    cdef long i = 0, j = 0

    if period >= size:
        return result

    s = sx = sxx = sy = syy = 0.0

    x = (1 - period) / 2.0
    for i in range(period):
        y = x * x
        s += 1
        sx += x
        sy += y
        sxx += x*x
        syy += y*y
        x += 1.0

    vxx = (sxx / s - sx * sx / s / s )
    vyy = (syy / s - sy * sy / s / s )

    if vxx <= 0 or vyy <= 0:
        return result

    for j in range(period - 1, size):
        skip = False

        sz = sxz = szz = 0.0
        x = (1 - period) / 2.0
        i = j - period + 1
        while i <= j:
            z = zs[i]
            if isnan(z):
                skip = True
                break
            sz += z
            sxz += x * z
            szz += z * z
            i += 1
            x += 1.0

        if skip:
            continue

        vxz = (sxz / s - sx * sz / s / s)
        vzz = (szz / s - sz * sz / s / s)

        slope = vxz / vxx

        if option == QUADREG_SLOPE:
            output[j] = slope
            continue

        sz = syz = szz = 0.0
        x = (1 - period) / 2.0
        i = j - period + 1
        while i <= j:
            y = x * x
            z = zs[i] - slope * x
            if isnan(z):
                skip = True
                break
            sz += z
            syz += y * z
            szz += z * z
            i += 1
            x += 1.0

        if skip:
            continue

        vyz = (syz / s - sy * sz / s / s)
        vzz = (szz / s - sz * sz / s / s)

        curve = vyz / vyy
        rvalue = vyz / math.sqrt(vyy * vzz) if vyy * vzz > 0 else NAN
        mse = (1.0 - rvalue * rvalue) * vzz
        rmse = math.sqrt(mse) if mse >= 0 else NAN


        if option == QUADREG_CURVE:
            output[j] = curve
            continue

        if option == QUADREG_RVALUE:
            output[j] = rvalue
            continue

        if option == QUADREG_RSQUARE:
            output[j] = rvalue * rvalue
            continue

        if option == QUADREG_RMSERROR:
            output[j] = rmse
            continue

    if wrap:
        result = wrap_result(result, series)

    return result



def calc_curve(series, long period=20, *, bint wrap=False):
    """ Curve (quadratic regression) """

    return quadratic_regression(series, period=period, option=QUADREG_CURVE, wrap=wrap)

