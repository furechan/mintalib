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


def test_ker_uses_period_changes():
    import numpy as np

    series = np.arange(1.0, 16.0)

    result = core.calc_ker(series, 3)

    assert np.isnan(result[:3]).all()
    assert result[3:] == pytest.approx(1.0)


def test_ker_bridges_nulls():
    import numpy as np

    series = np.array([1.0, 2.0, np.nan, 4.0, 3.0, 6.0, 8.0])

    result = core.calc_ker(series, 3)

    expected = core.calc_ker(series[~np.isnan(series)], 3)
    assert result[~np.isnan(result)] == pytest.approx(expected[~np.isnan(expected)])


def test_roc_scales_percentage_and_rocp_preserves_fraction():
    import numpy as np

    series = np.array([100.0, 110.0, 99.0])

    assert core.calc_roc(series, 1) == pytest.approx([np.nan, 10.0, -10.0], nan_ok=True)
    assert core.calc_rocp(series, 1) == pytest.approx([np.nan, 0.1, -0.1], nan_ok=True)


@pytest.mark.parametrize("name", ["calc_roc", "calc_rocp"])
def test_rate_of_change_rejects_negative_period(name):
    func = getattr(core, name)

    with pytest.raises(ValueError, match="Invalid period value -1"):
        func([100.0, 110.0], -1)


def test_natr_is_scaled_atr_over_close(prices):
    import numpy as np

    close = np.asarray(prices["close"], float)

    result = core.calc_natr(prices, 14)
    expected = 100 * core.calc_atr(prices, 14) / close

    assert result == pytest.approx(expected, nan_ok=True)


def test_bbp_and_bbw_are_unscaled_ratios():
    import numpy as np

    series = np.arange(1.0, 11.0)
    upper, middle, lower = core.calc_bbands(series, 5, 2.0)

    expected_bbp = (series - lower) / (upper - lower)
    expected_bbw = (upper - lower) / middle

    assert core.calc_bbp(series, 5, 2.0) == pytest.approx(expected_bbp, nan_ok=True)
    assert core.calc_bbw(series, 5, 2.0) == pytest.approx(expected_bbw, nan_ok=True)
