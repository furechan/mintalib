""" Balance of Power """

@add_metadata(inputs=('open', 'high', 'low', 'close'))
def calc_bop(open, high, low, close):
    """
    Balance of Power
    """

    cdef const double[:] open_view = np.asarray(open, float)
    cdef const double[:] high_view = np.asarray(high, float)
    cdef const double[:] low_view = np.asarray(low, float)
    cdef const double[:] close_view = np.asarray(close, float)

    cdef long size = check_size(open_view, high_view, low_view, close_view)
    cdef object result = np.empty(size, float)
    cdef double[:] output = result
    cdef double spread = NAN
    cdef long i = 0

    with nogil:
        for i in range(size):
            spread = high_view[i] - low_view[i]
            if spread != 0.0:
                output[i] = (close_view[i] - open_view[i]) / spread
            else:
                output[i] = NAN

    return result
