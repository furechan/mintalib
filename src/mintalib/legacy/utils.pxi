#cython: language_level=3

import numpy as np

from libc.math cimport isnan, sqrt

cdef double NAN = float('nan')


def export(target):
    name = getattr(target, "__name__", str(target))
    globals().setdefault('__all__', []).append(name)
    return target

@export
def hello(name="world"):
    """ hello world function (for diagnostic purposes) """

    return "Hello %s!" % name

@export
def float_array(double[:] xs):
    """ passthrough float array argument (for diagnostic purposes) """

    return xs

@export
def crossover(data, double level=0.0, bint wrap=True):
    """ value of 1 when data cross over level, 0.0 elsewhere """

    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, 0, dtype=int)
    cdef int[:] output = result

    cdef double prev = NAN, value = NAN

    cdef long i=0

    for i in range(size):
        value = xs[i]

        if value > level >= prev:
            output[i] = 1

        if not isnan(value):
            prev = value

    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result

@export
def crossunder(data, double level=0.0, bint wrap=True):
    """ value of 1 when data cross under level, 0.0 elsewhere """

    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, 0, dtype=int)
    cdef int[:] output = result

    cdef double prev = NAN, value = NAN
    cdef long i = 0

    for i in range(size):
        value = xs[i]

        if value < level <= prev:
            output[i] = 1

        if not isnan(value):
            prev = value

    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result



@export
def flag_above(series, double level=0.0, *, double nan_flag=NAN, bint wrap=True):
    """ returns flag for strictly positive values """

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value=NAN
    cdef double flag=NAN
    cdef long i=0

    for i in range(size):
        value = xs[i]

        if isnan(value):
            flag = nan_flag
        elif value > level:
            flag = 1.0
        else:
            flag = 0.0

        output[i] = flag

    if wrap and hasattr(series, '__array_wrap__'):
        result = series.__array_wrap__(result)

    return result


@export
def flag_below(series, double level=0.0, *, double nan_flag=NAN, bint wrap=True):
    """ returns flag for strictly negative values  """

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value=NAN
    cdef double flag=NAN
    cdef long i=0

    for i in range(size):
        value = xs[i]

        if isnan(value):
            flag = nan_flag
        elif value < level:
            flag = 1.0
        else:
            flag = 0.0

        output[i] = flag

    if wrap and hasattr(series, '__array_wrap__'):
        result = series.__array_wrap__(result)

    return result


@export
def invert_flag(series, *, double nan_flag=NAN, bint wrap=True):
    """ returns flag for strictly negative values  """

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value=NAN
    cdef double flag=NAN
    cdef long i=0

    for i in range(size):
        value = xs[i]

        if isnan(value):
            flag = nan_flag
        elif value > 0:
            flag = 0.0
        else:
            flag = 1.0

        output[i] = flag

    if wrap and hasattr(series, '__array_wrap__'):
        result = series.__array_wrap__(result)

    return result



@export
def where_flag(flag, x, y, z=NAN, *, bint wrap=True):
    """ returns signal according to value vis a vis up & down levels """

    cdef const double[:] fs = np.asarray(flag, float)

    cdef long size = fs.size

    cdef const double[:] xs = np.broadcast_to(np.float_(x), size)
    cdef const double[:] ys = np.broadcast_to(np.float_(y), size)
    cdef const double[:] zs = np.broadcast_to(np.float_(z), size)

    result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value = NAN
    cdef double fval = NAN
    cdef long i=0

    for i in range(size):
        fval = fs[i]

        if fval > 0:
            value = xs[i]
        elif fval <= 0:
            value = ys[i]
        else:
            value = zs[i]

        output[i] = value

    if wrap and hasattr(flag, '__array_wrap__'):
        result = flag.__array_wrap__(result)

    return result



@export
def flag_updown(series, double up_level=0.0, double down_level=0.0, *,
                double up_flag=1.0, double down_flag=0.0, double start_flag=NAN,
                bint wrap=True):
    """ returns flag according to value crossing up & down levels """

    cdef double[:] xs = np.asarray(series, float)
    cdef long size = xs.size

    result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double value=NAN, prev=NAN
    cdef double flag=start_flag
    cdef long i=0

    for i in range(size):
        value = xs[i]

        if value > up_level >= prev:
            flag = up_flag
        elif value <= down_level < prev:
            flag = down_flag

        output[i] = flag

        if not isnan(value):
            prev = value

    if wrap and hasattr(series, '__array_wrap__'):
        result = series.__array_wrap__(result)

    return result


@export
def timed_exit(buy, int max_holding, double buy_side=1.0, double sell_side=0.0):
    """ returns a net position array from buy signals with timed exits """

    cdef int[:] xs = np.asarray(buy, int)
    cdef long size = xs.size

    result = np.full(size, 0.0)
    cdef double[:] output = result

    cdef double pos = 0.0
    cdef long i = 0, j=0

    for i in range(size):
        j += 1
        if xs[i] > 0:
            pos = buy_side
            j = 0
        elif j >= max_holding:
            pos = 0
        output[i] = pos

    return result


@export
def net_position(buy, sell, long min_holding=0, long max_holding=0):
    """ returns a net position array from buy and sell signals """

    cdef int[:] xs = np.asarray(buy, int)
    cdef int[:] ys = np.asarray(sell, int)

    cdef long size = xs.size

    if ys.size != xs.size:
        raise ValueError("buy and sell must have same size!")

    result = np.full(size, 0.0)
    cdef double[:] output = result

    cdef double pos = 0.0
    cdef long i = 0, n = 0
    cdef bint sell_pending = 0

    for i in range(size):
        if xs[i] > 0:
            sell_pending = 0
            pos = 1.0
            n = 0

        elif pos > 0:
            n += 1

            if ys[i] > 0:
                if n < min_holding:
                    sell_pending = 1
                else:
                    pos = 0.0

            elif sell_pending and n >= min_holding:
                pos = 0.0

            elif max_holding and n >= max_holding:
                pos = 0.0

        output[i] = pos

    return result


@export
def rolling_yield(data, double n, bint wrap=True):
    """ attempt at calculating some smoothed yield from dividends """

    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double alpha = 2.0 / (n + 1.0)
    cdef double factor = n * alpha
    cdef double v=NAN, div_avg=0.0, div_acc=0.0
    cdef long i=0, skip=int(n)

    for i in range(size):
        v = xs[i]
        if not isnan(v):
            div_acc += v
            skip -= 1
        div_avg += alpha * (div_acc - div_avg)
        div_acc *= (1 - alpha)
        if skip <= 0:
            output[i] = div_avg * factor

    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result


@export
def calc_nav(price, position, *, double start_value=100.0, bint wrap=True):
    """ calculates net aset value from prices and positions """

    cdef double[:] _prc = np.asarray(price, float)
    cdef double[:] _pos = np.asarray(position, float)

    cdef long size = _prc.size

    if _prc.size != _pos.size:
        raise ValueError("arrays have a different size!")

    result = np.full(size, NAN)
    cdef double[:] output = result

    cdef double prc = NAN, pprc = NAN, chg = NAN
    cdef double pos = NAN, ppos = NAN, nav = NAN

    cdef long i = 0

    for i in range(size):
        prc = _prc[i]
        pos = _pos[i]

        if isnan(prc):
            continue

        if isnan(pos):
            continue

        if isnan(ppos):
            nav = start_value
        elif pprc > 0:
            chg = prc / pprc - 1.0
            nav *= 1 + chg * ppos

        pprc = prc
        ppos = pos

        output[i] = nav


    if wrap and hasattr(price, '__array_wrap__'):
        result = price.__array_wrap__(result)

    return result


@export
def max_drawdown(price):
    """ max drawdown from series of prices """

    cdef double[:] _prc = np.asarray(price, float)

    cdef long size = _prc.size

    cdef double prc = NAN, ath = NAN, dd = NAN, mdd = NAN

    cdef long i = 0

    for i in range(size):
        prc = _prc[i]

        if isnan(prc):
            pass
        elif isnan(ath):
            ath = prc
            mdd = 0.0
        else:
            dd = (prc/ath - 1.0)
            if dd < mdd:
                mdd = dd

    return mdd

