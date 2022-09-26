from pytest import mark, fixture

import numpy as np
import pandas as pd

from mintalib import core
from mintalib import testing


def ref_mad(series, period):
    mad = lambda s: np.mean(np.fabs(s - np.mean(s)))
    return series.rolling(window=period).apply(mad, raw=True)



@mark.parametrize("period", [5])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_mad(item, period):
    series = testing.sample_series(item)
    res = core.calc_mad(series, period=period)
    exp = ref_mad(series, period=period)
    assert np.allclose(res, exp, equal_nan=True)
