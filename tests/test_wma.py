from pytest import mark, fixture

import numpy as np
import pandas as pd

from mintalib import core
from mintalib import testing


def ref_wma(series, period: int = 10):
    weights = np.arange(1, period + 1, dtype=float)
    weights /= np.sum(weights)

    def average(data):
        return np.sum(data.values * weights)

    return series.rolling(period).apply(average)


@mark.parametrize("period", [5])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_wma(item, period):
    series = testing.sample_series(item)
    res = core.calc_wma(series, period=period)
    exp = ref_wma(series, period=period)
    assert np.allclose(res, exp, equal_nan=True)
