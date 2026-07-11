import pytest

from mintalib import core
from mintalib.samples import sample_prices
from mintalib.testing import first_param, sample_params

from importlib.util import find_spec

has_pandas = find_spec("pandas") is not None
has_polars = find_spec("polars") is not None


def list_core_functions():
    return [
        k for k, v in vars(core).items()
        if k.startswith(("calc_", "flag_"))
        and callable(v)
        and first_param(v) in ("prices", "series")
    ]


@pytest.fixture(params=[
    pytest.param("pandas", marks=pytest.mark.skipif(not has_pandas, reason="requires pandas")),
    pytest.param("polars", marks=pytest.mark.skipif(not has_polars, reason="requires polars")),
])
def prices(request):
    return sample_prices(backend=request.param)


@pytest.mark.parametrize("name", list_core_functions())
def test_core(name, prices):
    func = getattr(core, name)
    ftype = first_param(func)
    kwds = sample_params(func)
    data = prices
    if ftype == "series":
        data = data["close"]
    result = func(data, **kwds)
    assert result is not None


def test_rsi_bridges_nulls():
    import numpy as np

    series = np.arange(1.0, 31.0)
    series[16:] -= 5.0
    gapped = series.copy()
    gapped[15] = np.nan

    result = core.calc_rsi(gapped, 14)

    # the move across the gap must be measured
    assert result[-1] < 100.0
    # bridging a null is equivalent to removing it from the series
    expected = core.calc_rsi(np.delete(series, 15), 14)
    assert result[-1] == pytest.approx(expected[-1])
