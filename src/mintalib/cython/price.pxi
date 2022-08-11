""" Exponential Moving Average """


@export
def calc_avgprice(prices):
    """ Average Price """

    op, hi, lo, cl = extract_items(prices, ('open', 'high', 'low', 'close'))

    cdef double[:] _op = np.asarray(op, float)
    cdef double[:] _hi = np.asarray(hi, float)
    cdef double[:] _lo = np.asarray(lo, float)
    cdef double[:] _cl = np.asarray(cl, float)

    cdef long size = _cl.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (_op[i] + _hi[i] + _lo[i] + _cl[i]) / 4.0
        output[i] = v

    if isinstance(prices, DataFrame):
        result = make_series(result, prices)

    return result


@export
def calc_typprice(prices):
    """ Typical Price """

    hi, lo, cl = extract_items(prices, ('high', 'low', 'close'))

    cdef double[:] _hi = np.asarray(hi, float)
    cdef double[:] _lo = np.asarray(lo, float)
    cdef double[:] _cl = np.asarray(cl, float)

    cdef long size = _cl.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (_hi[i] + _lo[i] + _cl[i]) / 3.0
        output[i] = v

    if isinstance(prices, DataFrame):
        result = make_series(result, prices)

    return result

@export
def calc_wclprice(prices):
    """ Weighted Close Price """

    hi, lo, cl = extract_items(prices, ('high', 'low', 'close'))

    cdef double[:] _hi = np.asarray(hi, float)
    cdef double[:] _lo = np.asarray(lo, float)
    cdef double[:] _cl = np.asarray(cl, float)

    cdef long size = _cl.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (_hi[i] + _lo[i] + 2 * _cl[i]) / 4.0
        output[i] = v

    if isinstance(prices, DataFrame):
        result = make_series(result, prices)

    return result


@export
def calc_medprice(prices):
    """ Median Price """

    hi, lo = extract_items(prices, ('high', 'low'))

    cdef double[:] _hi = np.asarray(hi, float)
    cdef double[:] _lo = np.asarray(lo, float)

    cdef long size = _hi.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v
    cdef long i

    for i in range(size):
        v = (_hi[i] + _lo[i]) / 2.0
        output[i] = v

    if isinstance(prices, DataFrame):
        result = make_series(result, prices)

    return result



@export
class PRICE(Indicator):
    """ Price Indicator """

    def __init__(self, item='close'):
        self.item = item

    def calc(self, data):
        result = self.get_series(data)
        return result



@export
class AVGPRICE(Indicator):
    """ Average Price Indicator """

    def __init__(self, item='close'):
        self.item = item

    def calc(self, prices):
        result = calc_avgprice(prices)
        return result

@export
class TYPPRICE(Indicator):
    """ Typical Price Indicator """

    def __init__(self, item='close'):
        self.item = item

    def calc(self, prices):
        result = calc_typprice(prices)
        return result


@export
class WCLPRICE(Indicator):
    """ Weighted Close Price Indicator """

    def __init__(self, item='close'):
        self.item = item

    def calc(self, prices):
        result = calc_wclprice(prices)
        return result


@export
class MEDPRICE(Indicator):
    """ Median Price Indicator """

    def __init__(self, item='close'):
        self.item = item

    def calc(self, prices):
        result = calc_medprice(prices)
        return result




