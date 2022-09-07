from pytest import mark, fixture

import numpy as np
import pandas as pd

from mintalib import testing
from mintalib import core


@fixture(params=[20])
def period(request):
    return request.param


@fixture(params=['close', 'change'])
def item(request):
    return request.param


@mark.parametrize("period", [1])
@mark.parametrize("item", ['close', 'change'])
def test_roc(period, item):
    series = testing.sample_series(item)
    res = core.calc_roc(series, period=period)
    roc = series.pct_change(period, fill_method=None)
    roc = roc.replace([np.inf, -np.inf], np.nan)
    assert np.allclose(res, roc, equal_nan=True)
