""" Price """

@add_metadata(inputs=('open', 'high', 'low', 'close'))
def calc_avgprice(open, high, low, close):
    """
    Average Price

    Value of (open + high + low + close) / 4
    """

    cdef const double[:] open_view = np.asarray(open, float)
    cdef const double[:] high_view = np.asarray(high, float)
    cdef const double[:] low_view = np.asarray(low, float)
    cdef const double[:] close_view = np.asarray(close, float)

    cdef long size = check_size(open_view, high_view, low_view, close_view)
    cdef object result = np.empty(size, float)
    cdef double[:] output = result
    cdef long i = 0

    with nogil:
        for i in range(size):
            output[i] = (
                open_view[i] + high_view[i] + low_view[i] + close_view[i]
            ) / 4.0

    return result

@add_metadata(inputs=('high', 'low', 'close'))
def calc_typprice(high, low, close):
    """
    Typical Price

    Value of (high + low + close ) / 3
    """

    cdef const double[:] high_view = np.asarray(high, float)
    cdef const double[:] low_view = np.asarray(low, float)
    cdef const double[:] close_view = np.asarray(close, float)

    cdef long size = check_size(high_view, low_view, close_view)
    cdef object result = np.empty(size, float)
    cdef double[:] output = result
    cdef long i = 0

    with nogil:
        for i in range(size):
            output[i] = (high_view[i] + low_view[i] + close_view[i]) / 3.0

    return result

@add_metadata(inputs=('high', 'low', 'close'))
def calc_wclprice(high, low, close):
    """
    Weighted Close Price

    Value of (high + low + 2 * close) / 4
    """

    cdef const double[:] high_view = np.asarray(high, float)
    cdef const double[:] low_view = np.asarray(low, float)
    cdef const double[:] close_view = np.asarray(close, float)

    cdef long size = check_size(high_view, low_view, close_view)
    cdef object result = np.empty(size, float)
    cdef double[:] output = result
    cdef long i = 0

    with nogil:
        for i in range(size):
            output[i] = (
                high_view[i] + low_view[i] + 2.0 * close_view[i]
            ) / 4.0

    return result

@add_metadata(inputs=('high', 'low'))
def calc_medprice(high, low):
    """
    Median Price

    Value of (high + low) / 2
    """

    cdef const double[:] high_view = np.asarray(high, float)
    cdef const double[:] low_view = np.asarray(low, float)

    cdef long size = check_size(high_view, low_view)
    cdef object result = np.empty(size, float)
    cdef double[:] output = result
    cdef long i = 0

    with nogil:
        for i in range(size):
            output[i] = (high_view[i] + low_view[i]) / 2.0

    return result
