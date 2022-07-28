""" slope """



export('SlopeOption')
cpdef enum SlopeOption:
    SLOPE_DEFAULT = 0
    SLOPE_VALUE = 1
    SLOPE_INTERCEPT = 2
    SLOPE_CORRELATION = 3
    SLOPE_RMSERROR = 4
    SLOPE_FORECAST = 5
    SLOPE_BADOPTION = 6


@export
def calc_slope(series, int period=20, int option=0, int offset=0):
    """ Slope (linear regression with time) """

    if option == 0:
        option = SLOPE_VALUE

    if option < 0 or option >= SLOPE_BADOPTION:
        raise ValueError("Invalid option %d" % option)

    cdef double[:] ys = np.asarray(series, float)
    cdef long size = ys.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x, y, s, sx, sy, sxy, sxx, syy, vxy, vxx, vyy
    cdef double corr, slope, intercept, mse, rmse, forecast

    cdef long i = 0, j = 0

    if size < period:
        return result

    x = s = sx = sxx = 0.0
    for i in range(period):
        x += 1.0
        s += 1
        sx += x
        sxx += x*x

    vxx = (sxx / s - sx * sx / s / s )

    if vxx <= 0:
        return result

    if size <= period:
        return result

    for j in range(period-1, size):

        x = sy = sxy = syy = 0.0
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
            corr = vxy / sqrt(vxx * vyy) if vyy > 0 else NAN
            mse = vyy * (1 - corr * corr)
            rmse = sqrt(mse) if mse >= 0 else NAN

            if option == SLOPE_VALUE:
                output[j] = slope
            elif option == SLOPE_INTERCEPT:
                output[j] = intercept
            elif option == SLOPE_CORRELATION:
                output[j] = corr
            elif option == SLOPE_RMSERROR:
                output[j] = rmse
            elif option == SLOPE_FORECAST:
                forecast = intercept + slope * (period + offset)
                output[j] = forecast

    if isinstance(series, Series):
        result = make_series(result, series)

    return result



@export
class SLOPE(Indicator):
    """ Time Regression Slope """

    def __init__(self, period=20, *, item=None):
        self.period = period
        self.item = item

    def calc(self, data):
        series = self.get_series(data)
        result = calc_slope(series, self.period, option=SLOPE_VALUE)
        return result


    class RVALUE(Indicator):
        """ Time Regression R-value """

        def __init__(self, period=20, *, item=None):
            self.period = period
            self.item = item

        def calc(self, data):
            series = self.get_series(data)
            result = calc_slope(series, self.period, option=SLOPE_CORRELATION)
            return result


    class RMSE(Indicator):
        """ Time Regression Root Mean Square Error """

        def __init__(self, period=20, *, item=None):
            self.period = period
            self.item = item

        def calc(self, data):
            series = self.get_series(data)
            result = calc_slope(series, self.period, option=SLOPE_RMSERROR)
            return result


    class TSF(Indicator):
        """ Time Series Forecast """

        same_scale = True

        def __init__(self, period=20, offset=0, *, item=None):
            self.period = period
            self.offset = offset
            self.item = item

        def calc(self, data):
            series = self.get_series(data)
            result = calc_slope(series, self.period, opiton=SLOPE_FORECAST, offset=self.offset)
            return result
