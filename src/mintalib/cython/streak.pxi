""" Streak """


def calc_streak(series):
    """
    Consecutive streak of values above zero
    """

    cdef const double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double value = NAN
    cdef double streak = NAN

    cdef long i = 0

    for i in range(size):
        value = xs[i]

        if value > 0:
            streak += 1 
        else:
            streak = 0

        output[i] = streak

    return result

