from pytest import mark, fixture

import numpy as np
import pandas as pd

from mintalib import core
from mintalib import testing

def ref_max(series, period: int):
    result = series.rolling(window=period, min_periods=0).max()
    result[:period - 1] = np.nan
    return result



@mark.parametrize("period", [5])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_max(item, period):
    series = testing.sample_series(item)
    res = core.calc_max(series, period=period)
    exp = ref_max(series, period=period)
    assert np.allclose(res, exp, equal_nan=True)
