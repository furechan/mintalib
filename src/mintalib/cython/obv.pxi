""" On-Balance Volume """


@add_metadata(inputs=('close', 'volume'))
def calc_obv(close, volume):
    """
    On-Balance Volume

    Adds volume when close rises, subtracts volume when close falls, and carries
    the previous value when close is unchanged. The first value is initialized
    with the first volume.
    """

    cdef const double[:] cl = np.asarray(close, float)
    cdef const double[:] vol = np.asarray(volume, float)
    cdef long size = check_size(cl, vol)

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double value = NAN
    cdef double prev_close = NAN
    cdef double current_close = NAN
    cdef double current_volume = NAN
    cdef long i = 0
    cdef bint initialized = False

    with nogil:
        for i in range(size):
            current_close = cl[i]
            current_volume = vol[i]

            if isnan(current_close) or isnan(current_volume):
                continue

            if not initialized:
                value = current_volume
                initialized = True
            elif current_close > prev_close:
                value += current_volume
            elif current_close < prev_close:
                value -= current_volume

            output[i] = value
            prev_close = current_close

    return result
