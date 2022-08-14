""" testing utilities """

import inspect
import warnings

import numpy as np
import pandas as pd

from functools import lru_cache

from . import reflib
from .. import core
from .. import utils

SAMPLE_SIZE = 260


def export(func):
    globals().setdefault('__all__', []).append(func.__name__)
    return func


@lru_cache
def sample_prices(count=SAMPLE_SIZE):
    prices = utils.sample_prices(count)
    prices['change'] = prices.close.pct_change(1)
    return prices


def get_sample(item=None, *, skip=0):
    """ sample prices dataframe or series if item is specified """

    result = sample_prices().copy()

    if item is not None:
        result = result[item]

    if skip > 0:
        result.iloc[:skip] = np.nan

    if skip < 0:
        result.iloc[skip:] = np.nan

    return result


def compare_results(result, target):
    return np.allclose(result, target, equal_nan=True)


def merge_results(result, target):
    if isinstance(result, pd.Series) and isinstance(target, pd.Series):
        return pd.DataFrame(dict(result=result, target=target))

    if isinstance(result, pd.DataFrame) and isinstance(target, pd.DataFrame):
        return result.join(target, rsuffix="2")

    return result, target


def get_function(name):
    return getattr(core, f"calc_{name}", None)


@export
def test_function(name, *args, item=None, verbose=False, **kwargs):
    calc = get_function(name)
    ref = reflib.get_ref(name) if reflib else None

    if ref is None:
        warnings.warn(f"Ref for {name} not found!")
        return

    if item is None:
        param = next(k for k in inspect.signature(calc).parameters.keys())
        if param == 'series':
            item = 'close'

    data = get_sample(item)

    result = calc(data, *args, **kwargs)
    target = ref(data, *args, **kwargs)

    compare = compare_results(result, target)

    if verbose:
        print(merge_results(result, target))

    return compare
