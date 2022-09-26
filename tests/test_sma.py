from pytest import mark, fixture

import numpy as np
import pandas as pd

from mintalib import core
from mintalib import testing


def ref_sma(series, period: int):
    return series.rolling(window=period).mean()


@mark.parametrize("period", [5])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_sma(item, period):
    series = testing.sample_series(item)
    res = core.calc_sma(series, period=period)
    exp = ref_sma(series, period=period)
    assert np.allclose(res, exp, equal_nan=True)
