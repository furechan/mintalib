""" Money Flow Index """

@add_metadata(inputs=('high', 'low', 'close', 'volume'))
def calc_mfi(high, low, close, volume, long period=14):
    """
    Money Flow Index

    Args:
        period (int): time period, default 14
    """

    if period <= 0:
        raise ValueError("period must be greater than zero")

    high = np.asarray(high, float)
    low = np.asarray(low, float)
    close = np.asarray(close, float)
    volume = np.asarray(volume, float)

    cdef long input_size = check_size(high, low, close, volume)

    typ = (high + low + close) / 3.0
    flow_arr = typ * volume * np.sign(np.diff(typ, prepend=NAN))

    cdef const double[:] flow = flow_arr
    cdef long size = flow.shape[0]

    cdef object result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double v = NAN, old = NAN
    cdef double psum = 0.0, nsum = 0.0
    cdef long i = 0, count = 0

    with nogil:
        for i in range(size):
            v = flow[i]

            if isnan(v):
                psum = 0.0
                nsum = 0.0
                count = 0
                continue

            if v > 0.0:
                psum += v
            elif v < 0.0:
                nsum -= v

            count += 1

            if count > period:
                old = flow[i - period]
                if old > 0.0:
                    psum -= old
                elif old < 0.0:
                    nsum += old
                count -= 1

            if count == period:
                if nsum > 0.0:
                    output[i] = 100.0 - 100.0 / (1.0 + psum / nsum)
                elif psum > 0.0:
                    output[i] = 100.0

    return result
