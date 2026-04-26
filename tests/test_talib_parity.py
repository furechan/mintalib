"""Cross-validation of mintalib calc_* functions against TA-Lib.

Covers indicators that produce bit-for-bit identical results.

Known non-matches (excluded):
  DEMA/TEMA/MACD/NATR/ADX - different EMA initialization (converge after ~150 bars)

Convergence tests (checked from bar 200 onward):
  ATR - same algorithm as talib, values converge after EMA warm-up (~150 bars)
  KAMA, SAR                        - different algorithm
  STOCH                            - different default parameters
  TSF                              - talib projects one bar ahead (use offset=1 to match)
  ROC                              - talib multiplies by 100; mintalib returns fraction
  BBANDS                           - talib uses close; mintalib uses typical price
  BOP                              - talib has no period smoothing
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


def test_stdev(prices):
    c = prices.close.values.astype(float)
    check(talib.STDDEV(c, 20), core.calc_stdev(c, 20))


def test_mad(prices):
    c = prices.close.values.astype(float)
    check(talib.AVGDEV(c, 14), core.calc_mad(c, 14))


def test_cci(prices, hlcv):
    h, lo, c, _ = hlcv
    check(talib.CCI(h, lo, c, 20), core.calc_cci(prices, 20))


def test_mfi(prices, hlcv):
    h, lo, c, v = hlcv
    check(talib.MFI(h, lo, c, v, 14), core.calc_mfi(prices, 14))


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


def test_slope(prices):
    c = prices.close.values.astype(float)
    check(talib.LINEARREG_SLOPE(c, 20), core.calc_slope(c, 20))


def test_tsf(prices):
    c = prices.close.values.astype(float)
    # talib TSF projects one bar ahead; match with offset=1
    check(talib.TSF(c, 20), core.calc_tsf(c, 20, offset=1))


