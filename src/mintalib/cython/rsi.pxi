""" Relative Strength Index """


def calc_rsi(series, long period=14):
    """
    Relative Strength Index

    Args:
        period (int) : time period, default 14
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef object ups_arr = np.full(size, np.nan)
    cdef object dns_arr = np.full(size, np.nan)
    cdef double[:] ups = ups_arr
    cdef double[:] dns = dns_arr

    cdef double v = NAN, pv = NAN, dv = NAN
    cdef long i = 0

    for i in range(size):
        v = xs[i]
        if v == v and pv == pv:
            dv = v - pv
            ups[i] = dv if dv > 0.0 else 0.0
            dns[i] = -dv if dv < 0.0 else 0.0
        pv = v

    cdef const double[:] rma_ups = calc_rma(ups_arr, period)
    cdef const double[:] rma_dns = calc_rma(dns_arr, period)

    cdef double u = NAN, d = NAN
    for i in range(size):
        u = rma_ups[i]
        d = rma_dns[i]
        if u == u and d == d and d > 0:
            output[i] = 100.0 - (100.0 / (1.0 + u / d))
        elif u == u and d == d:
            output[i] = 100.0

    return result
