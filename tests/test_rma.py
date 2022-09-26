from pytest import mark, fixture

import numpy as np
import pandas as pd

from mintalib import core
from mintalib import testing


def ref_rma(series, period):
    if period <= 0:
        raise ValueError(f"Invalid period {period}")

    result = []
    rma = np.nan
    total = count = 0
    for v in series:
        if np.isnan(v):
            pass
        elif count < period:
            total += v
            count += 1
            if count >= period:
                rma = total / count
        else:
            rma += (v - rma) / period
        result.append(rma)
    result = pd.Series(result, index=series.index)
    return result


@mark.parametrize("period", [5])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_rma(item, period):
    series = testing.sample_series(item)
    res = core.calc_rma(series, period=period)
    exp = ref_rma(series, period=period)
    assert np.allclose(res, exp, equal_nan=True)
