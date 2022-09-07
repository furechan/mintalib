from pytest import mark, fixture

import numpy as np
import pandas as pd

from mintalib import core
from mintalib import testing
from mintalib.testing import reflib


def ref_stdev(series, period: int):
    return series.rolling(window=period).std(ddof=0)



@mark.parametrize("period", [5])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_stdev(item, period):
    series = testing.sample_series(item)
    res = core.calc_stdev(series, period=period)
    exp = ref_stdev(series, period=period)
    assert np.allclose(res, exp, equal_nan=True)
