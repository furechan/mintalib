"""Cross-validation of mintalib calc_* functions against TA-Lib.

Covers indicators that produce bit-for-bit identical results.

Known non-matches (excluded):
  DEMA/TEMA/MACD/NATR/ADX - different EMA initialization (converge after ~150 bars)

Convergence tests (checked from bar 200 onward):
  ATR - same algorithm as talib, values converge after EMA warm-up (~150 bars)
  KAMA, SAR                        - different algorithm
  STOCH                            - different default parameters
  LINREG                           - talib TSF projects one bar ahead (use offset=1 to match)
"""

import numpy as np
import pytest

talib = pytest.importorskip("talib")

from mintalib import core  # noqa: E402
from mintalib.samples import sample_prices  # noqa: E402


@pytest.fixture(scope="module")
def prices():
    return sample_prices()


@pytest.fixture(scope="module")
def hlcv(prices):
    h = prices.high.values.astype(float)
    lo = prices.low.values.astype(float)
    c = prices.close.values.astype(float)
    v = prices.volume.values.astype(float)
    return h, lo, c, v


def check(ta, our, rtol=1e-5, atol=1e-8):
    our = np.asarray(our)
    mask = ~(np.isnan(ta) | np.isnan(our))
    assert mask.any()
    assert np.allclose(ta[mask], our[mask], rtol=rtol, atol=atol)


def test_ema(prices):
    c = prices.close.values.astype(float)
    check(talib.EMA(c, 20)[200:], core.calc_ema(c, 20)[200:])

def test_sma(prices):
    c = prices.close.values.astype(float)
    check(talib.SMA(c, 20), core.calc_sma(c, 20))


def test_wma(prices):
    c = prices.close.values.astype(float)
    check(talib.WMA(c, 20), core.calc_wma(c, 20))


def test_rsi(prices):
    c = prices.close.values.astype(float)
    check(talib.RSI(c, 14), core.calc_rsi(c, 14))


def test_rsi_flat_series():
    c = np.ones(30)
    np.testing.assert_allclose(talib.RSI(c, 14), core.calc_rsi(c, 14), equal_nan=True)


def test_roc(prices):
    c = prices.close.values.astype(float)
    check(talib.ROC(c, 10), core.calc_roc(c, 10))


def test_roc_signed_values_and_zero_denominator():
    c = np.array([-100.0, -110.0, -90.0, 0.0, 10.0])
    np.testing.assert_allclose(talib.ROC(c, 1), core.calc_roc(c, 1), equal_nan=True)


def test_stdev(prices):
    c = prices.close.values.astype(float)
    check(talib.STDDEV(c, 20), core.calc_stdev(c, 20))


def test_bbands(prices):
    c = prices.close.values.astype(float)
    upper, middle, lower = talib.BBANDS(c, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    our_upper, our_middle, our_lower = core.calc_bbands(c, 20, 2.0)
    check(upper, our_upper)
    check(middle, our_middle)
    check(lower, our_lower)


def test_mad(prices):
    c = prices.close.values.astype(float)
    check(talib.AVGDEV(c, 14), core.calc_mad(c, 14))


def test_cci(prices, hlcv):
    h, lo, c, _ = hlcv
    check(talib.CCI(h, lo, c, 20), core.calc_cci(prices, 20))


def test_mfi(prices, hlcv):
    h, lo, c, v = hlcv
    check(talib.MFI(h, lo, c, v, 14), core.calc_mfi(prices, 14))


def test_bop(prices):
    o = prices.open.values.astype(float)
    h = prices.high.values.astype(float)
    lo = prices.low.values.astype(float)
    c = prices.close.values.astype(float)
    check(talib.BOP(o, h, lo, c), core.calc_bop(prices))


def test_obv(prices):
    c = prices.close.values.astype(float)
    v = prices.volume.values.astype(float)
    check(talib.OBV(c, v), core.calc_obv(c, v))


def test_max(prices):
    c = prices.close.values.astype(float)
    check(talib.MAX(c, 20), core.calc_max(c, 20))


def test_min(prices):
    c = prices.close.values.astype(float)
    check(talib.MIN(c, 20), core.calc_min(c, 20))


def test_sum(prices):
    c = prices.close.values.astype(float)
    check(talib.SUM(c, 20), core.calc_sum(c, 20))


def test_typprice(prices, hlcv):
    h, lo, c, _ = hlcv
    check(talib.TYPPRICE(h, lo, c), core.calc_typprice(prices))


def test_wclprice(prices, hlcv):
    h, lo, c, _ = hlcv
    check(talib.WCLPRICE(h, lo, c), core.calc_wclprice(prices))


def test_avgprice(prices, hlcv):
    h, lo, c, _ = hlcv
    o = prices.open.values.astype(float)
    check(talib.AVGPRICE(o, h, lo, c), core.calc_avgprice(prices))


def test_trange(prices, hlcv):
    h, lo, c, _ = hlcv
    check(talib.TRANGE(h, lo, c), core.calc_trange(prices))


def test_atr(prices, hlcv):
    h, lo, c, _ = hlcv
    check(talib.ATR(h, lo, c, 14)[200:], core.calc_atr(prices, 14)[200:])


def test_natr(prices, hlcv):
    h, lo, c, _ = hlcv
    check(talib.NATR(h, lo, c, 14)[200:], core.calc_natr(prices, 14)[200:])


def test_linreg_slope(prices):
    c = prices.close.values.astype(float)
    check(talib.LINEARREG_SLOPE(c, 20), core.calc_linreg_slope(c, 20))


def test_linreg(prices):
    c = prices.close.values.astype(float)
    check(talib.LINEARREG(c, 20), core.calc_linreg(c, 20))
    # talib TSF projects one bar ahead; match with offset=1
    check(talib.TSF(c, 20), core.calc_linreg(c, 20, offset=1))
