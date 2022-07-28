""" cython fincalc """


import numpy as np

from libc.math cimport fabs, isnan, log

cdef double NAN = float('nan')

def export(target):
    name = getattr(target, "__name__", str(target))
    globals().setdefault('__all__', []).append(name)
    return target


@export
def calc_ema(data, double n, wrap=True):
    """ exponential moving average """

    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double alpha = 2.0 / (n + 1.0)
    cdef double v = NAN, ema = NAN
    cdef long i = 0, skip = int(n)

    for i in range(size):
        v = xs[i]

        if not isnan(v):
            skip -= 1
            if isnan(ema):
                ema = v
            else:
                ema += alpha * (v - ema)

        if skip <= 0:
            output[i] = ema

    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result


@export
def calc_sma(data, int n, wrap=True):
    """ simple moving average """

    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double v = NAN, rsum = 0
    cdef long i = 0, j = 0, count = 0

    for i in range(size):
        v = xs[i]

        if not isnan(v):
            rsum += v
            count += 1

        while count > n and j < i:
            v, j = xs[j], j+1
            if not isnan(v):
                rsum -= v
                count -= 1

        if count >= n:
            output[i] = rsum / count

    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result


@export
def calc_rma(data, int n, wrap=True):
    """ rsi style moving average """

    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double alpha = 1.0 / n
    cdef double v = NAN, rsum = 0, rma = NAN
    cdef long i = 0, j = 0, count = 0

    for i in range(size):
        v = xs[i]

        if isnan(v):
            pass

        elif isnan(rma):
            if count < n:
                rsum += v
                count += 1
            else:
                rma = rsum / count

        else:
            rma += alpha * (v - rma)

        output[i] = rma

    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result

@export
def calc_wma(data, int n, wrap=True):
    """ simple moving average """

    cdef double[:] xs = np.asarray(data)
    cdef long size = xs.size

    cdef object result = np.full(size, np.nan)

    if n > size:
        return result

    cdef double[:] output = result

    cdef double divisor = n * (n + 1) / 2
    cdef double v=NAN, sum=NAN
    cdef long i=0, j=0


    for i in range(size - n + 1):
        sum = 0.0

        for j in range(n):
            v = xs[i + j]

            if isnan(v):
                break

            sum += v * (j+1)
        else:
            output[i + j] = sum / divisor

    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result


@export
def calc_rsi(data, int n=14, wrap=True):
    """ Calculates relative strength index """

    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double alpha = 1.0 / n
    cdef double v = NAN, pv = NAN, dv = NAN
    cdef double up = NAN, down = NAN, ups = 0.0, downs = 0.0, rsi = NAN
    cdef long i = 0, count = 0

    for i in range(size):
        v = xs[i]

        if isnan(v):
            pass

        elif isnan(pv):
            pv = v

        else:
            dv, pv = v - pv, v
            up, down= (dv, 0.0) if dv>=0.0 else (0.0, -dv)

            if count < n:
                count += 1
                ups += up * alpha
                downs += down * alpha
                continue

            ups += (up - ups) * alpha
            downs += (down - downs) * alpha

            if downs > 0:
                rsi = 100.0 - (100.0 / (1.0 + ups / downs))

        if not isnan(rsi):
            output[i] = rsi

    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result


@export
def calc_trange(prices, *, bint log_prices=False, bint percent=False, bint wrap=True):
    """ Calculates true range """

    cdef double[:] high = np.asarray(prices.high, float)
    cdef double[:] low = np.asarray(prices.low, float)
    cdef double[:] close = np.asarray(prices.close, float)

    cdef long size = close.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double h = NAN, l = NAN, c = NAN, pc = NAN, tr = NAN

    cdef long i = 0

    for i in range(size):
        c = close[i]
        h = high[i]
        l = low[i]

        if isnan(c):
            continue

        if log_prices:
            c = log(c)
            h = log(h)
            l = log(l)

        if pc > h:
            h = pc
        elif pc < l:
            l = pc

        pc = c
        tr = h - l

        if percent:
            tr *= 100 / c

        output[i] = tr

    if wrap and hasattr(prices.close, '__array_wrap__'):
        result = prices.close.__array_wrap__(result)

    return result


@export
def calc_atr(prices, int n=14, *, log_prices=False, percent=False, wrap=True):
    """ calculates average true range """
    tr = calc_trange(prices, log_prices=log_prices, percent=percent, wrap=wrap)
    atr = calc_rma(tr, n, wrap=wrap)
    return atr


@export
def parabolic_sar(prices, double afs=0.02, double maxaf=0.2, wrap=True):
    """ calculates Parabolic SAR """

    cdef double[:] high = np.asarray(prices.high, float)
    cdef double[:] low = np.asarray(prices.low, float)
    cdef double[:] close = np.asarray(prices.close, float)

    cdef long size = close.size

    result = np.full(size, np.nan, dtype=float)
    cdef double[:] output = result

    cdef double sar = NAN, ep = NAN, af = NAN
    cdef double hi = NAN, lo = NAN

    cdef long direction = 0
    cdef long i = 0

    for i in range(size):
        hi, lo = high[i], low[i]

        if not direction:
            sar, ep, af = lo, hi, afs
            direction = +1

        elif direction > 0 and lo < sar:
            sar, ep, af = ep, hi, afs
            direction = -1

        elif direction < 0 and hi > sar:
            sar, ep, af = ep, lo, afs
            direction = +1

        output[i] = sar

        sar += af * (ep-sar)

        if direction > 0 and hi > ep:
            af += afs
            ep = hi

        if direction < 0 and lo < ep:
            af += afs
            ep = lo

        if maxaf and af > maxaf:
            af = maxaf

    if wrap and hasattr(prices.close, '__array_wrap__'):
        result = prices.close.__array_wrap__(result)

    return result


@export
def parabolic_stop(prices, entry,
        double stop_loss=0.0, double stop_atr=0.0,
        double afs=0.02, double maxaf=0.20, wrap=True):
    """ calculates position with parabolic stop """

    cdef double[:] high = np.asarray(prices.high, float)
    cdef double[:] low = np.asarray(prices.low, float)
    cdef double[:] close = np.asarray(prices.close, float)
    cdef long size = close.size

    cdef long[:] xs = np.asarray(entry, int)
    if xs.size != size:
        raise ValueError("array sizes doe not match!")

    cdef double[:] atr = calc_atr(prices)

    result = np.full(size, 0.0, dtype=float)
    cdef double[:] output = result

    cdef double pos=0.0, stop=NAN, ep=NAN, af=NAN
    cdef long i=0

    for i in range(size):
        hi, lo, cl = high[i], low[i], close[i]

        if xs[i] > 0 :
            pos = 1.0
            af, stop, ep= afs, lo, hi
            if stop_loss:
                stop *= (1 - stop_loss)
            if stop_atr:
                stop -= stop_atr * atr[i]
            if stop < 0:
                stop = 0.0

        elif pos > 0:
            if lo <= stop:
                pos = 0.0

        else:
            continue

        output[i] = pos
        stop += af * (ep-stop)

        if hi > ep:
            ep = hi
            af += afs

        if maxaf and af > maxaf:
            af = maxaf

    if wrap and hasattr(prices.close, '__array_wrap__'):
        result = prices.close.__array_wrap__(result)

    return result



@export
def efficiency_ratio(data, int n=10, wrap=True):

    cdef double[:] xs = np.asarray(data, float)
    cdef long size = xs.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double x = NAN, px = NAN, dx = NAN
    cdef double y = NAN, py = NAN, dy = NAN

    cdef double erval = NAN, ernum = NAN, erdiv = 0

    cdef long ercnt = 0
    cdef long i = 0, j = 0

    for i in range(size):
        x = xs[i]

        if isnan(x):
            continue

        dx, px = x - px, x

        if isnan(dx):
            continue

        erdiv += fabs(dx)
        ercnt += 1

        while ercnt >= n:
            y, j = xs[j], j+1

            if isnan(y):
                continue

            dy, py = y - py, y

            ernum = fabs(x-y)
            erval = ernum / erdiv if erdiv else 1.0

            if not isnan(dy):
                erdiv -= fabs(dy)
                ercnt -= 1

        output[i] = erval


    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result



@export
def calc_kama(data, int n=10, double fastn=2.0, double slown=30.0, wrap=True):

    cdef double[:] xs = np.asarray(data, float)
    cdef double[:] ers = efficiency_ratio(xs, n)
    cdef long size = xs.size

    result = np.full(size, np.nan)
    cdef double[:] output = result

    cdef double fastf = 2.0 / (fastn + 1.0)
    cdef double slowf = 2.0 / (slown + 1.0)
    cdef double alpha = NAN
    cdef double value = NAN
    cdef double kama = NAN
    cdef double er = NAN

    cdef long i = 0

    for i in range(size):
        value = xs[i]
        er = ers[i]

        if isnan(value) or isnan(er):
            continue

        alpha = (slowf + er * (fastf - slowf)) ** 2.0

        if isnan(kama):
            kama = value
        elif not isnan(alpha):
            kama += alpha * (value - kama)

        output[i] = kama


    if wrap and hasattr(data, '__array_wrap__'):
        result = data.__array_wrap__(result)

    return result


