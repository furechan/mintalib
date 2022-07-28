""" utilities """

import sys
import numpy as np
import pandas as pd
import datetime as dt


def export(func):
    frame = sys._getframe(1)
    exports = frame.f_globals.setdefault('__all__', [])
    name = getattr(func, '__name__', None) or str(func)
    if name not in exports:
        exports.append(name)
    return func


@export
def date_range(count=260, freq='B', start_date=None, end_date=None):
    """ quick date_range utility (wrapper aoutn pandas functoin of same name) """

    if not start_date and not end_date:
        end_date = dt.date.today()

    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)

    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    dates = pd.date_range(periods=count, start=start_date, end=end_date, freq=freq)

    return dates


@export
def wipe_data(data, skip=None):
    if skip is None:
        return data

    if isinstance(skip, tuple):
        head, tail = skip
    elif isinstance(skip, int):
        head, tail = (skip, 0) if skip >= 0 else (0, -skip)
    else:
        raise ValueError(f"Invalid skip value {skip!r}")

    if head > 0:
        data.iloc[:head] = np.nan

    if tail > 0:
        data.iloc[-tail:] = np.nan

    return data


@export
def random_walk(count=260, freq='B', start_value=100.0,
                volatility=0.20, fwd_rate=0.10,
                start_date=None, end_date=None,
                name='price', skip=None, seed=None):
    """ generates a single series of random walk prices """

    generator = np.random.default_rng(seed)

    dates = date_range(count, freq=freq, start_date=start_date, end_date=end_date)

    days = (dates.max() - dates.min()).days
    sampling = (365.0 * count / days)
    fwd = np.log(1 + fwd_rate) / sampling
    std = volatility / np.sqrt(sampling)

    change = generator.standard_normal(count - 1) * std + np.log(1 + fwd)
    price = start_value * np.exp(np.r_[0.0, change.cumsum(0)])

    series = pd.Series(price, index=dates.values, name=name).rename_axis(index='date')

    if skip is not None:
        wipe_data(series, skip)

    return series


@export
def sample_prices(count=260, freq='B', start_value=100.0,
                  volatility=0.20, fwd_rate=0.10,
                  start_date=None, end_date=None,
                  skip=None, seed=None):
    """ generates a dataframe of random walk prices """

    if not start_date and not end_date:
        end_date = dt.date.today()

    generator = np.random.default_rng(seed)

    dates = date_range(count, freq=freq, start_date=start_date, end_date=end_date)

    days = (dates.max() - dates.min()).days
    sampling = (4.0 * 365.0 * count / days)
    fwd = np.log(1 + fwd_rate) / sampling
    std = volatility / np.sqrt(sampling)

    rnd = generator.standard_normal((count, 4)).cumsum(1) * std + fwd
    cum = np.r_[0.0, rnd[:, -1].cumsum(0)[:-1]]

    op = start_value * np.exp(rnd[:, 0] + cum)
    hi = start_value * np.exp(rnd.max(1) + cum)
    lo = start_value * np.exp(rnd.min(1) + cum)
    cl = start_value * np.exp(rnd[:, -1] + cum)

    vol = np.exp(generator.standard_normal(count) * 0.2 + 1.0) * 50000.0

    data = dict()
    data['date'] = dates.values
    data['open'] = np.around(op, 2)
    data['high'] = np.around(hi, 2)
    data['low'] = np.around(lo, 2)
    data['close'] = np.around(cl, 2)
    data['volume'] = vol.astype(int)

    prices = pd.DataFrame(data).set_index('date')

    if skip is not None:
        wipe_data(prices, skip)

    return prices
