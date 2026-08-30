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
        if k.startswith("calc_")
        and callable(v)
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
    if ftype == "series":
        args = (prices["close"],)
    else:
        inputs = func.metadata["inputs"]
        args = tuple(prices[name] for name in inputs)
    result = func(*args, **kwds)
    assert result is not None


def test_rsi_bridges_nulls():
    import numpy as np

    series = np.arange(1.0, 31.0)
    series[16:] -= 5.0
    gapped = series.copy()
    gapped[15] = np.nan

    result = core.calc_rsi(gapped, 14)

    # the null is passed through without resetting the previous-price or RMA state
    assert np.isnan(result[15])
    # the move across the gap must be measured
    assert result[-1] < 100.0
    # bridging a null is equivalent to removing it from the series
    expected = core.calc_rsi(np.delete(series, 15), 14)
    assert result[-1] == pytest.approx(expected[-1])


def test_obv():
    import numpy as np

    close = np.array([10.0, 11.0, 11.0, 9.0, 12.0])
    volume = np.array([100.0, 20.0, 30.0, 40.0, 50.0])

    result = core.calc_obv(close, volume)

    np.testing.assert_array_equal(result, [100.0, 120.0, 120.0, 80.0, 130.0])


def test_obv_bridges_nulls():
    import numpy as np

    close = np.array([10.0, np.nan, 12.0, 11.0, 9.0])
    volume = np.array([100.0, 20.0, 30.0, np.nan, 40.0])

    result = core.calc_obv(close, volume)

    np.testing.assert_allclose(
        result,
        [100.0, np.nan, 130.0, np.nan, 90.0],
        equal_nan=True,
    )


def test_obv_empty_and_different_sizes():
    import numpy as np

    assert core.calc_obv(np.array([]), np.array([])).size == 0

    with pytest.raises(ValueError, match="Different sizes"):
        core.calc_obv(np.ones(2), np.ones(3))


def test_cmf_treats_zero_range_as_zero_money_flow():
    import numpy as np

    high = np.array([10.0, 12.0, 12.0])
    low = np.array([10.0, 10.0, 10.0])
    close = np.array([10.0, 12.0, 10.0])
    volume = np.array([100.0, 100.0, 100.0])

    result = core.calc_cmf(high, low, close, volume, 2)

    np.testing.assert_allclose(result, [np.nan, 0.5, 0.0], equal_nan=True)


def test_rsi_flat_series_is_zero_after_initialization():
    import numpy as np

    result = core.calc_rsi(np.ones(20), 14)

    assert np.isnan(result[:14]).all()
    assert result[14:] == pytest.approx(0.0)


def test_rate_of_change_is_nan_when_previous_value_is_zero():
    import numpy as np

    series = np.array([0.0, 2.0, 4.0])

    np.testing.assert_allclose(
        core.calc_roc(series, 1), [np.nan, np.nan, 100.0], equal_nan=True
    )
    np.testing.assert_allclose(
        core.calc_rocp(series, 1), [np.nan, np.nan, 1.0], equal_nan=True
    )


def test_standalone_directional_indexes_match_dmi(prices):
    import numpy as np

    high, low, close = prices["high"], prices["low"], prices["close"]
    dmi = core.calc_dmi(high, low, close, 14)

    np.testing.assert_allclose(core.calc_adx(high, low, close, 14), dmi[0], equal_nan=True)
    np.testing.assert_allclose(core.calc_pdi(high, low, close, 14), dmi[1], equal_nan=True)
    np.testing.assert_allclose(core.calc_mdi(high, low, close, 14), dmi[2], equal_nan=True)


def test_rma_preserves_nulls_while_bridging_state():
    import numpy as np

    series = np.array([1.0, 2.0, np.nan, 4.0])

    result = core.calc_rma(series, 2)
    expected = core.calc_rma(series[~np.isnan(series)], 2)

    assert np.isnan(result[2])
    assert result[[0, 1, 3]] == pytest.approx(expected, nan_ok=True)
    assert core.calc_rma(series, 1) == pytest.approx(series, nan_ok=True)


@pytest.mark.parametrize("name", ["calc_ema", "calc_dema", "calc_tema", "calc_hma", "calc_zlema"])
def test_moving_average_period_one_is_identity(name):
    import numpy as np

    series = np.array([1.0, 2.0, np.nan, 4.0])

    assert getattr(core, name)(series, 1) == pytest.approx(series, nan_ok=True)


@pytest.mark.parametrize("matype", ["sma", "ema", "wma", "hma", "dema", "tema"])
def test_mav_uses_lowercase_matype(matype):
    import numpy as np

    series = np.arange(1.0, 31.0)

    result = core.calc_mav(series, 5, matype=matype)
    expected = getattr(core, f"calc_{matype}")(series, 5)

    assert result == pytest.approx(expected, nan_ok=True)


def test_mav_rejects_uppercase_matype():
    import numpy as np

    with pytest.raises(ValueError, match="Invalid matype EMA"):
        core.calc_mav(np.arange(1.0, 11.0), 5, matype="EMA")


@pytest.mark.parametrize("name", ["calc_ema", "calc_dema", "calc_tema"])
def test_ema_family_preserves_nulls_while_bridging_state(name):
    import numpy as np

    series = np.array([1.0, 2.0, 3.0, 4.0, 5.0, np.nan, 7.0, 8.0, 9.0, 10.0])
    valid = ~np.isnan(series)
    func = getattr(core, name)

    result = func(series, 3)
    expected = func(series[valid], 3)

    assert np.isnan(result[~valid]).all()
    assert result[valid] == pytest.approx(expected, nan_ok=True)


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


def test_roc_supports_signed_values_and_returns_nan_for_zero_denominator():
    import numpy as np

    series = np.array([-100.0, -110.0, -90.0, 0.0, 10.0])

    assert core.calc_roc(series, 1) == pytest.approx(
        [np.nan, 10.0, -18.18181818181818, -100.0, np.nan], nan_ok=True
    )
    assert core.calc_rocp(series, 1) == pytest.approx(
        [np.nan, 0.1, -0.1818181818181818, -1.0, np.nan], nan_ok=True
    )


@pytest.mark.parametrize(
    "name",
    ["calc_roc", "calc_rocp", "calc_lroc", "calc_diff", "calc_lag"],
)
@pytest.mark.parametrize("period", [-1, 0])
def test_offset_functions_reject_non_positive_period(name, period):
    func = getattr(core, name)

    with pytest.raises(ValueError, match="period must be greater than zero"):
        func([100.0, 110.0], period)


def test_natr_is_scaled_atr_over_close(prices):
    import numpy as np

    close = np.asarray(prices["close"], float)

    result = core.calc_natr(prices["high"], prices["low"], close, 14)
    expected = 100 * core.calc_atr(prices["high"], prices["low"], close, 14) / close

    assert result == pytest.approx(expected, nan_ok=True)


def test_bbp_and_bbw_are_unscaled_ratios():
    import numpy as np

    series = np.arange(1.0, 11.0)
    upper, middle, lower = core.calc_bbands(series, 5, 2.0)

    expected_bbp = (series - lower) / (upper - lower)
    expected_bbw = (upper - lower) / middle

    assert core.calc_bbp(series, 5, 2.0) == pytest.approx(expected_bbp, nan_ok=True)
    assert core.calc_bbw(series, 5, 2.0) == pytest.approx(expected_bbw, nan_ok=True)


def test_bop_is_raw_per_bar(prices):
    import numpy as np

    with np.errstate(all="ignore"):
        raw = (
            (np.asarray(prices["close"], float) - np.asarray(prices["open"], float))
            / (np.asarray(prices["high"], float) - np.asarray(prices["low"], float))
        )

    assert core.calc_bop(
        prices["open"], prices["high"], prices["low"], prices["close"]
    ) == pytest.approx(raw, nan_ok=True)
