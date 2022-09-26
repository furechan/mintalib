from pytest import mark, fixture

import numpy as np
import pandas as pd

from mintalib import core
from mintalib import testing


def ref_roc(series, period: int):
    roc = series.pct_change(period, fill_method=None)
    roc = roc.replace([np.inf, -np.inf], np.nan)
    return roc



@mark.parametrize("period", [1])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_roc(item, period):
    series = testing.sample_series(item)
    res = core.calc_roc(series, period=period)
    exp = ref_roc(series, period=period)
    assert np.allclose(res, exp, equal_nan=True)
