""" Curve """



export('CurveOption')
cpdef enum CurveOption:
    CURVE_VALUE = 1
    CURVE_SLOPE = 1
    CURVE_INTERCEPT = 3
    CURVE_MSE = 10
    CURVE_RMSE = 11
    CURVE_RSQUARE = 12
    CURVE_RVALUE = 13
    CURVE_BADOPTION = 14


@export
def calc_curve(series, int period=20, int option=0, int offset=0):
    """ Curve (curvilinear regression with time) """

    if option == 0:
        option = CURVE_VALUE

    if option < 0 or option >= CURVE_BADOPTION:
        raise ValueError("Invalid option %d" % option)

    cdef double[:] zs = np.asarray(series, float)
    cdef long size = zs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, sx, sxx, vxx
    cdef double y, sy, syy, vyy
    cdef double z, sz, szz, vzz
    cdef double s, sxz, vxz, syz, vyz
    cdef double sse
    cdef double e = NAN

    cdef double slope, curve, intercept, tail, mse, rmse, rvalue, rsquare

    cdef bint skip = 0

    cdef long i = 0, j = 0

    if size < period:
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

        if option == CURVE_SLOPE:
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

        if option == CURVE_VALUE:
            output[j] = curve
            continue

        if option == CURVE_INTERCEPT:
            x = (period - 1) / 2.0 + offset
            z = intercept + slope * x + curve * x * x
            output[j] = z
            continue

        sse = 0.0
        x = (1 - period) / 2.0
        i = j - period + 1
        while i <= j:
            z = zs[i]
            if isnan(e):
                skip = True
                break
            e = z - slope * x - curve * x * x  - intercept
            sse += e * e
            i += 1
            x += 1.0

        if skip:
            continue

        mse = sse / s
        rmse = sqrt(mse) if mse >= 0 else NAN
        rsquare = 1 - mse / vzz
        rvalue = sqrt(rsquare) if rsquare >= 0 else NAN

        if option == CURVE_MSE:
            output[j] = mse
            continue

        if option == CURVE_RMSE:
            output[j] = rmse
            continue

        if option == CURVE_RSQUARE:
            output[j] = rsquare
            continue

        if option == CURVE_RVALUE:
            output[j] = rvalue
            continue

    if isinstance(series, Series):
        result = make_series(result, series)

    return result


@export
class CURVE(Indicator):
    """ Curve (curvilinear regression) """

    def __init__(self, period=20, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_curve(series, self.period)
        return result

