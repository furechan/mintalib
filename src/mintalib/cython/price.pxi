""" Price """


@export
def calc_avgprice(prices):
    """ Average Price """

    cdef double[:] open = asarray(prices['open'], float)
    cdef double[:] high = asarray(prices['high'], float)
    cdef double[:] low = asarray(prices['low'], float)
    cdef double[:] close = asarray(prices['close'], float)

    cdef long size = check_size(open, high, low, close)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (open[i] + high[i] + low[i] + close[i]) / 4.0
        output[i] = v

    result = wrap_result(result, prices)

    return result


@export
def calc_typprice(prices):
    """ Typical Price """

    cdef double[:] high = asarray(prices['high'], float)
    cdef double[:] low = asarray(prices['low'], float)
    cdef double[:] close = asarray(prices['close'], float)

    cdef long size = check_size(high, low, close)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (high[i] + low[i] + close[i]) / 3.0
        output[i] = v

    result = wrap_result(result, prices)

    return result

@export
def calc_wclprice(prices):
    """ Weighted Close Price """

    cdef double[:] high = asarray(prices['high'], float)
    cdef double[:] low = asarray(prices['low'], float)
    cdef double[:] close = asarray(prices['close'], float)

    cdef long size = check_size(high, low, close)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (high[i] + low[i] + 2 * close[i]) / 4.0
        output[i] = v

    result = wrap_result(result, prices)

    return result


@export
def calc_midprice(prices):
    """ Mid Price """

    cdef double[:] high = asarray(prices['high'], float)
    cdef double[:] low = asarray(prices['low'], float)
    cdef long size = check_size(high, low)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (high[i] + low[i]) / 2.0
        output[i] = v

    result = wrap_result(result, prices)

    return result




class PRICE(Indicator):
    """ Price Indicator """

    def calc(self, data):
        result = self.get_series(data)
        return result



class AVGPRICE(Indicator):
    """ Average Price Indicator """

    def calc(self, prices):
        result = calc_avgprice(prices)
        return result


class TYPPRICE(Indicator):
    """ Typical Price Indicator """

    def calc(self, prices):
        result = calc_typprice(prices)
        return result



class WCLPRICE(Indicator):
    """ Weighted Close Price Indicator """

    def calc(self, prices):
        result = calc_wclprice(prices)
        return result



class MIDPRICE(Indicator):
    """ Mid Price Indicator """

    def calc(self, prices):
        result = calc_midprice(prices)
        return result




