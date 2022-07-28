""" fincalc native routines """

import numpy as np
import pandas as pd

from .numeric import calc_ema, calc_rma, calc_atr, calc_trange


# TODO do we need to rename pandas specific functions to distinguish them the numeric calc functions ?
# TODO do we need to rename summary calc functions to distinguish from the rolling calc functions ?


def export(func):
    globals().setdefault('__all__', []).append(func.__name__)
    return func


@export
def shift_array(data, n=1, fill_value=np.nan):
    """ Shifts numpy array by given offset """

    xs = np.asarray(data)
    result = np.empty_like(xs)

    if n > 0:
        result[:n] = fill_value
        result[n:] = xs[:-n]
    elif n < 0:
        result[n:] = fill_value
        result[:n] = xs[-n:]
    else:
        result[:] = xs

    return result


@export
def calc_mid(prices):
    """ Calculates mid prices (used in calc_price) """

    result = prices.filter(['high', 'low', 'close']).mean(axis=1).rename('mid')
    return result


@export
def calc_log(prices):
    """ Calculates log prices (used in calc_price) """

    return np.log(prices.close).rename('log')


@export
def calc_price(prices, item='close'):
    """ looks up or calculates standard item """

    if item in prices:
        return prices.get(item)

    if item == 'mid':
        return calc_mid(prices)

    if item == 'log':
        return calc_log(prices)

    raise ValueError(f"Invalid item {item}") from None


# TODO remove calc_ret and calc_logret or rename ?
# TODO rename calc_ret into calc_roc ?
# TODO rename calc_logret into calc_logdiff ?


@export
def calc_ret(series, n=1):
    """ Calculates return over number of periods """

    xs = np.asarray(series)
    ys = shift_array(xs, n)
    result = xs / ys - 1.0
    return result


@export
def calc_logret(series, n=1):
    """ Calculates log return over number of periods """

    xs = np.asarray(series)
    ys = shift_array(xs, n)
    result = np.log(xs / ys)
    return result


@export
def date_span(series, basis="365d", *, dropna=True):
    """ series date span relative to basis (requires datetimeindex) """

    if dropna:
        series = series.dropna()

    dates = series.index.get_level_values('date')

    if dates.empty:
        return np.nan

    sdate, edate = dates[0], dates[-1]

    span = (edate - sdate) / pd.Timedelta(basis)

    return span


@export
def date_sampling(series, basis="365d", *, dropna=True):
    """ series date sampling relative to basis (requires datetime index) """

    if dropna:
        series = series.dropna()

    dates = series.index.get_level_values('date')

    periods = dates.size - 1.0

    if periods <= 0:
        return np.nan

    sdate, edate = dates[0], dates[-1]

    span = (edate - sdate) / pd.Timedelta(basis)

    if span > 0:
        return periods / span

    return np.nan


@export
def calc_cagr(price):
    """ Compound Annual Growth Rate (requires datetimeindex) """

    price = price.dropna()

    if len(price) <= 1:
        return np.nan

    span = date_span(price)

    if not span > 0:
        return np.nan

    first = price.iloc[0]
    last = price.iloc[-1]

    if first <= 0 and last <= 0:
        raise ValueError("negative price")

    result = (last / first) ** (1 / span) - 1.0

    return result


@export
def calc_volatility(price):
    """ series volatility (requires a datetimeindex) ! """

    sampling = date_sampling(price, "365d")

    if not sampling > 0:
        return np.nan

    log_returns = price.apply(np.log).diff()
    result = log_returns.std() * np.sqrt(sampling)

    return result


@export
def calc_macd(series, n1=12, n2=26, n3=9, *, name='macd', relative=False):
    """ Calculates MACD """

    ema1 = calc_ema(series, n1)
    ema2 = calc_ema(series, n2)

    if relative:
        macd = 100 * (ema1 - ema2) / ema2
    else:
        macd = ema1 - ema2

    signal = calc_ema(macd, n3)
    hist = macd - signal

    result = dict()
    result[name] = macd
    result[name + "signal"] = signal
    result[name + "hist"] = hist

    result = pd.DataFrame(result, index=series.index)

    return result


@export
def calc_dema(series, n=50, wrap=True):
    """ Calculates double ema """

    ema1 = calc_ema(series, n)
    ema2 = calc_ema(ema1, n)

    result = 2 * ema1 - ema2

    if wrap and hasattr(series, '__array_wrap__'):
        result = series.__array_wrap__(result)

    return result


@export
def calc_tema(series, n=50, wrap=True):
    """ Calculates triple ema """

    ema1 = calc_ema(series, n)
    ema2 = calc_ema(ema1, n)
    ema3 = calc_ema(ema2, n)

    result = 3 * ema1 - 3 * ema2 + ema3

    if wrap and hasattr(series, '__array_wrap__'):
        result = series.__array_wrap__(result)

    return result


@export
def price_density(prices, window=20):
    """ Calculates price density (cf Kaufman) """

    trading_range = (prices.high - prices.low).abs().rolling(window).sum()
    high = prices.high.rolling(window).max()
    low = prices.low.rolling(window).min()
    result = trading_range / (high - low)

    return result


@export
def calc_adx(prices, period=14):
    """ Calculates ADX """

    hm = prices.high.diff()
    lm = -prices.low.diff()

    atr = calc_atr(prices, period)

    dm1 = np.where((hm > lm) & (hm > 0), hm, 0)
    dm2 = np.where((lm > hm) & (lm > 0), lm, 0)

    with np.errstate(divide='ignore'):
        di1 = 100 * calc_rma(dm1, period) / atr
        di2 = 100 * calc_rma(dm2, period) / atr
        dx = 100 * np.abs(di1 - di2) / (di1 + di2)

    adx = calc_rma(dx, period)

    return adx


@export
def tracking_error(prices, series, window=14, relative=True):
    """ Calculates average tracing error of an EMA as multiple of true range """

    delta = np.abs(series - prices.close)
    result = calc_rma(delta, window, wrap=True)

    if relative:
        atr = calc_atr(prices, window)
        return result / atr

    return result


@export
def calc_maverr(prices, window=20):
    """ Calculates average tracing error of an EMA as multiple of true range """

    tr = calc_trange(prices)
    ema = calc_ema(prices.close, window, wrap=True)
    err = calc_ema(np.abs(prices.close - ema), window, wrap=True)
    atr = calc_ema(tr, window, wrap=True)

    return err / atr
