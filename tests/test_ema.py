from pytest import mark, fixture

import numpy as np
import pandas as pd

from mintalib import core
from mintalib import testing
from mintalib.testing import reflib


def ref_ema(series, period: int, adjust: bool = False):
    kwds = dict(span=period, adjust=adjust, ignore_na=True, min_periods=period)
    return series.ewm(**kwds).mean()



@mark.parametrize("period", [5])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_ema(item, period):
    series = testing.sample_series(item)
    res = core.calc_ema(series, period=period)
    exp = ref_ema(series, period=period)
    assert np.allclose(res, exp, equal_nan=True)
