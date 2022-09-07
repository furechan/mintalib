""" testing utilities """

import inspect
import warnings

import numpy as np
import pandas as pd

from pathlib import Path

from functools import lru_cache

from . import reflib
from .. import core
from .. import utils
from .. import functions

SAMPLE_SIZE = 260


def export(func):
    globals().setdefault('__all__', []).append(func.__name__)
    return func


def data_file(name):
    data_folder = Path(__file__).joinpath("../data").resolve(True)
    path = data_folder.joinpath(name)
    return path


def create_sample(count=SAMPLE_SIZE):
    prices = utils.sample_prices(count)
    prices['change'] = prices.close.pct_change(1)
    return prices


@lru_cache
def sample_prices(skip=0):
    file = data_file("sample-prices.csv")
    prices = pd.read_csv(file, index_col=0, parse_dates=True)

    if skip > 0:
        prices.iloc[:skip] = np.nan

    if skip < 0:
        prices.iloc[skip:] = np.nan

    return prices


def sample_series(item=None, *, skip=0):
    """ sample prices dataframe or series if item is specified """

    if item is None:
        item = 'close'

    result = sample_prices().copy()

    if item is not None:
        result = result[item]

    if skip > 0:
        result.iloc[:skip] = np.nan

    if skip < 0:
        result.iloc[skip:] = np.nan

    return result


def get_sample(item=None, *, skip=0):
    """ sample prices dataframe or series if item is specified """

    warnings.warn(f"get_sample is deprecated, use sample_series instead", DeprecationWarning)

    return sample_series(item=item, skip=skip)


def compare_results(result, target):
    return np.allclose(result, target, equal_nan=True)


def merge_results(result, target):
    if isinstance(result, pd.Series) and isinstance(target, pd.Series):
        return pd.DataFrame(dict(result=result, target=target))

    if isinstance(result, pd.DataFrame) and isinstance(target, pd.DataFrame):
        return result.join(target, rsuffix="2")

    return result, target


@export
def test_core(name, *args, item=None, verbose=False, wrap=True, **kwargs):
    calc = getattr(core, f"calc_{name}", None)

    ref = reflib.get_ref(name)

    if ref is None:
        warnings.warn(f"Ref for {name} not found!")
        return

    if item is None:
        param = next(k for k in inspect.signature(calc).parameters.keys())
        if param == 'series':
            item = 'close'

    data = sample_series(item)

    kwds = dict()

    parameters = inspect.signature(calc).parameters

    if wrap and 'wrap' in parameters:
        kwds.update(wrap=True)

    result = calc(data, *args, **kwargs, **kwds)
    target = ref(data, *args, **kwargs)

    compare = compare_results(result, target)

    if verbose:
        print(merge_results(result, target))

    return compare


@export
def test_function(name, *args, item=None, verbose=False, **kwargs):
    calc = getattr(functions, name, None)

    ref = reflib.get_ref(name)

    if ref is None:
        warnings.warn(f"Ref for {name} not found!")
        return

    if item is None:
        param = next(k for k in inspect.signature(calc).parameters.keys())
        if param == 'series':
            item = 'close'

    data = sample_series(item)

    result = calc(data, *args, **kwargs)
    target = ref(data, *args, **kwargs)

    compare = compare_results(result, target)

    if verbose:
        print(merge_results(result, target))

    return compare
