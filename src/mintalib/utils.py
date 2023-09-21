""" utilities """


import numpy as np
import pandas as pd
import datetime as dt

from pathlib import Path


def data_file(name):
    """ local data file path """
    data_folder = Path(__file__).joinpath("../data").resolve(True)
    path = data_folder.joinpath(name)
    return path


def sample_prices(item: str = None, *, skip=0):
    """ sample prices dataframe or series """

    file = data_file("sample-prices.csv")
    prices = pd.read_csv(file, index_col=0, parse_dates=True)

    if skip > 0:
        prices.iloc[:skip] = np.nan

    if skip < 0:
        prices.iloc[skip:] = np.nan

    if item is not None:
        return prices[item]

    return prices


def date_range(count=260, freq='B', start_date=None, end_date=None):
    """ quick date_range utility (wrapper around pandas function of the same name) """

    if not start_date and not end_date:
        end_date = dt.date.today()

    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)

    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    dates = pd.date_range(periods=count, start=start_date, end=end_date, freq=freq)

    return dates


def random_walk(count: int = 260,
                freq: str = 'B',
                start_value: float = 100.0,
                volatility: float = 0.20,
                fwd_rate : float = 0.10,
                skip: int = 0,
                start_date=None,
                end_date=None,
                name=None,
                seed=None):
    """ generates a single series of random walk prices """

    generator = np.random.default_rng(seed)

    dates = date_range(count, freq=freq, start_date=start_date, end_date=end_date)

    days = (dates.max() - dates.min()).days
    sampling = (365.0 * count / days)
    fwd = np.log(1 + fwd_rate) / sampling
    std = volatility / np.sqrt(sampling)

    change = generator.standard_normal(count - 1) * std + np.log(1 + fwd)
    prices = start_value * np.exp(np.r_[0.0, change.cumsum(0)])

    if skip:
        prices[:skip] = np.nan

    result = pd.Series(prices, index=dates.values, name=name).rename_axis(index='date')

    return result


def random_prices(count=260, freq='B', start_value=100.0,
                  volatility=0.20, fwd_rate=0.10,
                  start_date=None, end_date=None,
                  seed=None, index=True, as_dict=False):
    """ generates a dataframe of random prices """

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

    if index:
        data['date'] = dates.values

    data['open'] = np.around(op, 2)
    data['high'] = np.around(hi, 2)
    data['low'] = np.around(lo, 2)
    data['close'] = np.around(cl, 2)
    data['volume'] = vol.astype(int)

    if as_dict:
        return data

    prices = pd.DataFrame(data)

    if index:
        prices = prices.set_index('date')

    return prices
