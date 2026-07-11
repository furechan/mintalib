"""Numeric verification of the LINREG/QUADREG statistics against numpy.polyfit.

Each rolling statistic is recomputed per-window with an explicit polynomial fit:
  LINREG          - value of the regression line at the last bar (offset projects forward)
  LINREG_SLOPE    - slope of the regression line
  LINREG_RVALUE   - correlation coefficient
  LINREG_RMSE     - root mean square error of the linear fit
  QUADREG         - value of the regression parabola at the last bar (offset projects forward)
  QUADREG_CURVE   - quadratic coefficient
  QUADREG_SLOPE   - derivative of the parabola at the last bar (offset projects forward)
  QUADREG_RVALUE  - partial correlation of the quadratic term, given the linear term
  QUADREG_RMSE    - root mean square error of the quadratic fit
"""

import numpy as np
import pytest

from mintalib import core
from mintalib.samples import sample_prices

PERIOD = 20
OFFSET = 5


@pytest.fixture(scope="module")
def series():
    return sample_prices().close.values.astype(float)[:300]


def rolling_ref(series, period, stat):
    """Compute a rolling regression statistic with explicit per-window polyfit."""
    size = len(series)
    result = np.full(size, np.nan)
    x = np.arange(period, dtype=float)
    for i in range(period - 1, size):
        w = series[i - period + 1 : i + 1]
        result[i] = stat(x, w)
    return result


def linfit(x, w):
    slope, intercept = np.polyfit(x, w, 1)
    return slope, intercept


def quadfit(x, w):
    curve, slope, intercept = np.polyfit(x, w, 2)
    return curve, slope, intercept


def partial_corr(x, w):
    """Correlation of the quadratic term with w, after removing the linear term."""
    u = x * x
    xc = x - x.mean()
    z = w - np.dot(xc, w) / np.dot(xc, xc) * x
    uz = u - np.dot(xc, u) / np.dot(xc, xc) * x
    zc, uc = z - z.mean(), uz - uz.mean()
    return np.dot(zc, uc) / np.sqrt(np.dot(zc, zc) * np.dot(uc, uc))


def check(result, expected):
    assert np.allclose(result, expected, rtol=1e-6, equal_nan=True)


def test_linreg(series):
    def stat(x, w, offset=0):
        slope, intercept = linfit(x, w)
        return intercept + slope * (x[-1] + offset)

    check(core.calc_linreg(series, PERIOD), rolling_ref(series, PERIOD, stat))
    check(
        core.calc_linreg(series, PERIOD, offset=OFFSET),
        rolling_ref(series, PERIOD, lambda x, w: stat(x, w, offset=OFFSET)),
    )


def test_linreg_slope(series):
    stat = lambda x, w: linfit(x, w)[0]  # noqa: E731
    check(core.calc_linreg_slope(series, PERIOD), rolling_ref(series, PERIOD, stat))


def test_linreg_rvalue(series):
    stat = lambda x, w: np.corrcoef(x, w)[0, 1]  # noqa: E731
    check(core.calc_linreg_rvalue(series, PERIOD), rolling_ref(series, PERIOD, stat))


def test_linreg_rmse(series):
    def stat(x, w):
        slope, intercept = linfit(x, w)
        return np.sqrt(np.mean((w - intercept - slope * x) ** 2))

    check(core.calc_linreg_rmse(series, PERIOD), rolling_ref(series, PERIOD, stat))


def test_quadreg(series):
    def stat(x, w, offset=0):
        curve, slope, intercept = quadfit(x, w)
        xe = x[-1] + offset
        return intercept + slope * xe + curve * xe * xe

    check(core.calc_quadreg(series, PERIOD), rolling_ref(series, PERIOD, stat))
    check(
        core.calc_quadreg(series, PERIOD, offset=OFFSET),
        rolling_ref(series, PERIOD, lambda x, w: stat(x, w, offset=OFFSET)),
    )


def test_quadreg_curve(series):
    stat = lambda x, w: quadfit(x, w)[0]  # noqa: E731
    check(core.calc_quadreg_curve(series, PERIOD), rolling_ref(series, PERIOD, stat))


def test_quadreg_slope(series):
    def stat(x, w, offset=0):
        curve, slope, _ = quadfit(x, w)
        return slope + 2 * curve * (x[-1] + offset)

    check(core.calc_quadreg_slope(series, PERIOD), rolling_ref(series, PERIOD, stat))
    check(
        core.calc_quadreg_slope(series, PERIOD, offset=OFFSET),
        rolling_ref(series, PERIOD, lambda x, w: stat(x, w, offset=OFFSET)),
    )


def test_quadreg_rvalue(series):
    check(core.calc_quadreg_rvalue(series, PERIOD), rolling_ref(series, PERIOD, partial_corr))


def test_quadreg_rmse(series):
    def stat(x, w):
        curve, slope, intercept = quadfit(x, w)
        return np.sqrt(np.mean((w - intercept - slope * x - curve * x * x) ** 2))

    check(core.calc_quadreg_rmse(series, PERIOD), rolling_ref(series, PERIOD, stat))
