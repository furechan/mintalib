"""
    Alternate implementation of indicators for reference/testing purposes
    Calculations are mostly pandas based
"""

import numpy as np
import pandas as pd


def calc_roc(series, period: int = 1):
    """Rate of Change"""
    roc = series.pct_change(period, fill_method=None)
    roc = roc.replace([np.inf, -np.inf], np.nan)
    return roc


def calc_ema(series, period: int, adjust: bool = False):
    """Exponential Moving Average"""
    kwds = dict(span=period, adjust=adjust, ignore_na=True, min_periods=period)
    return series.ewm(**kwds).mean()


def calc_sma(series, period: int):
    """Simple Moving Average"""
    return series.rolling(window=period).mean()


def calc_sum(series, period: int):
    """Rolling Sum"""
    return series.rolling(window=period).sum()


def calc_min(series, period: int):
    """Rolling Minimum"""
    return series.rolling(window=period).min()


def calc_max(series, period: int):
    """Rolling Maximum"""
    return series.rolling(window=period).max()


def calc_stdev(series, period: int):
    """Standard Deviation"""
    return series.rolling(window=period).std(ddof=0)


def calc_mad(series, period: int):
    """Mean Aasolute deviation"""

    def _mad(s):
        return np.mean(np.fabs(s - np.mean(s)))

    return series.rolling(window=period).apply(_mad, raw=True)


def calc_wma(series, period: int = 10):
    """Weighted Moving Average"""
    weights = np.arange(1, period + 1, dtype=float)
    weights /= np.sum(weights)

    def average(data):
        return np.sum(data.values * weights)

    return series.rolling(period).apply(average)


def calc_rsi(series, period: int = 14):
    """Relative Strength Index"""
    kw = dict(alpha=1.0 / period, min_periods=period, adjust=True, ignore_na=True)

    diff = series.diff()
    ups = diff.clip(lower=0).ewm(**kw).mean()
    downs = diff.clip(upper=0).abs().ewm(**kw).mean()
    result = 100.0 - (100.0 / (1.0 + ups / downs))

    return result


def calc_macd(series, n1: int = 12, n2: int = 26, n3: int = 9):
    """Moving Averrage Convergence Divergence"""

    ema1 = calc_ema(series, n1)
    ema2 = calc_ema(series, n2)

    macd = ema1 - ema2
    signal = calc_ema(macd, n3)
    hist = macd - signal

    result = dict(macd=macd, macdsignal=signal, macdhist=hist)

    return pd.DataFrame(result)


def calc_ppo(series, n1: int = 12, n2: int = 26, n3: int = 9):
    """Price percentage oscillator"""

    ema1 = calc_ema(series, n1)
    ema2 = calc_ema(series, n2)

    ppo = (ema1 / ema2 - 1.0) * 100
    signal = calc_ema(ppo, n3)
    hist = ppo - signal

    result = dict(ppo=ppo, pposignal=signal, ppohist=hist)

    return pd.DataFrame(result)


def calc_slope(series, period: int = 20):
    """Slope (time linear regression)"""

    xx = np.arange(period) - (period - 1) / 2.0

    def func(xs):
        if np.any(np.isnan(xs)):
            return np.nan

        return np.polyfit(xx, xs, 1)[0]

    return series.rolling(period).apply(func, raw=True)
