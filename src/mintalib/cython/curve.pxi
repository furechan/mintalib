""" slope """



cdef enum:
    CURVE_OPTION_CURVE = 0
    CURVE_OPTION_SLOPE = 1
    CURVE_OPTION_INTERCEPT = 2
    CURVE_OPTION_RMSE = 4
    CURVE_OPTION_RSQUARE = 5
    CURVE_OPTION_RVALUE = 6
    CURVE_OPTION_BADOPTION = 7



@export
class CurveOption(IntEnum):
    """ Slope Option Enumeration """
    def __repr__(self):
        return str(self)

    CURVE = 0
    SLOPE = 1
    INTERCEPT = 2
    RMSE = 4
    RSQUARE = 5
    RVALUE = 6
    BADOPTION = 7



@export
def calc_curve(series, long period=20, int option=0, int offset=0):
    """ Curve (time curvilinear regression) """

    if option < 0 or option >= CURVE_OPTION_BADOPTION:
        raise ValueError("Invalid option %d" % option)

    cdef double[:] zs = asarray(series, float)
    cdef long size = zs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, sx, sxx, vxx
    cdef double y, sy, syy, vyy
    cdef double z, sz, szz, vzz
    cdef double s, sxz, vxz, syz, vyz
    cdef double e, sse

    cdef double slope, curve, intercept, tail, mse, rmse, rvalue, rsquare

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

        sz = syz = 0.0
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
            i += 1
            x += 1.0

        if skip:
            continue

        vyz = (syz / s - sy * sz / s / s)

        curve = vyz / vyy
        intercept = (sz - curve * sy) / s

        if option == CURVE_OPTION_CURVE:
            output[j] = curve
            continue

        if option == CURVE_OPTION_INTERCEPT:
            x = (period - 1) / 2.0 + offset
            z = intercept + slope * x + curve * x * x
            output[j] = z
            continue

        sse = 0.0
        x = (1 - period) / 2.0
        i = j - period + 1
        while i <= j:
            z = zs[i]
            e = z - slope * x - curve * x * x  - intercept
            if isnan(e):
                skip = True
                break
            sse += e * e
            i += 1
            x += 1.0

        if skip:
            continue

        mse = sse / s
        rmse = sqrt(mse) if mse >= 0 else NAN
        rsquare = 1 - mse / vzz
        rvalue = sqrt(rsquare) if rsquare >= 0 else NAN

        if option == CURVE_OPTION_RMSE:
            output[j] = rmse
            continue

        if option == CURVE_OPTION_RSQUARE:
            output[j] = rsquare
            continue

        if option == CURVE_OPTION_RVALUE:
            output[j] = rvalue
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


    class RSQUARE(Indicator):
        """ Curve R-Square """

        def __init__(self, period: int = 20, *, item=None):
            self.period = period
            self.item = item

        def calc(self, data):
            series = self.get_series(data)
            result = calc_slope(series, self.period, option=CURVE_OPTION_RSQUARE)
            return result

