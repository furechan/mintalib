from pytest import mark, fixture

import numpy as np
import pandas as pd

from mintalib import core
from mintalib import testing
from mintalib.testing import reflib


def ref_min(series, period: int):
    result = series.rolling(window=period, min_periods=0).min()
    result[:period - 1] = np.nan
    return result



@mark.parametrize("period", [5])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_min(item, period):
    series = testing.sample_series(item)
    res = core.calc_min(series, period=period)
    exp = ref_min(series, period=period)
    assert np.allclose(res, exp, equal_nan=True)
