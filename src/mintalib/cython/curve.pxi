""" slope """



cdef enum:
    CURVE_OPTION_CURVE = 0
    CURVE_OPTION_SLOPE = 1
    CURVE_OPTION_RVALUE = 2
    CURVE_OPTION_RSQUARE = 3
    CURVE_OPTION_RMSERROR = 4
    CURVE_OPTION_BADOPTION = 5


@export
class CurveOption(IntEnum):
    """ Slope Option Enumeration """
    def __repr__(self):
        return str(self)

    CURVE = 0
    SLOPE = 1
    RVALUE = 2
    RSQUARE = 3
    RMSERROR = 4



@export
def calc_curve(series, long period=20, *, int option=0, int offset=0):
    """ Curve (time curvilinear regression) """

    if option < 0 or option >= CURVE_OPTION_BADOPTION:
        raise ValueError("Invalid option %d" % option)

    cdef double[:] zs = np.asarray(series, float)
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

        if option == SLOPE:
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
        intercept = (sz - curve * sy) / s
        rvalue = vyz / sqrt(vyy * vzz) if vyy * vzz > 0 else NAN
        mse = (1.0 - rvalue * rvalue) * vzz
        rmse = sqrt(mse) if mse >= 0 else NAN


        if option == CURVE_OPTION_CURVE:
            output[j] = curve
            continue

        if option == CURVE_OPTION_RVALUE:
            output[j] = rvalue
            continue

        if option == CURVE_OPTION_RSQUARE:
            output[j] = rvalue * rvalue
            continue

        if option == CURVE_OPTION_RMSERROR:
            output[j] = rmse
            continue

    result = wrap_result(result, series)

    return result



class CURVE(Indicator):
    """ Curve (time curvilinear regression) """

    def __init__(self, period : int = 20, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_curve(series, self.period, option=CURVE_OPTION_CURVE)
        return result


    class RVALUE(Indicator):
        """ Curve R-Value """

        def __init__(self, period: int = 20, *, item=None):
            self.period = period
            self.item = item

        def calc(self, data):
            series = self.get_series(data)
            result = calc_slope(series, self.period, option=CURVE_OPTION_RVALUE)
            return result


    class ERROR(Indicator):
        """ Curve Root Mean Square Error """

        def __init__(self, period: int = 20, *, item=None):
            self.period = period
            self.item = item

        def calc(self, data):
            series = self.get_series(data)
            result = calc_slope(series, self.period, option=CURVE_OPTION_RMSERROR)
            return result


