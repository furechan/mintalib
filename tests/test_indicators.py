import pytest

from mintalib import indicators
from mintalib.indicators import EMA, ROC, SMA
from mintalib.model.indicator import IndicatorChain
from mintalib.samples import sample_prices
from mintalib.testing import sample_params

from importlib.util import find_spec

has_pandas = find_spec("pandas") is not None
has_polars = find_spec("polars") is not None


def list_indicators():
    return [k for k, v in vars(indicators).items() if k.isupper() and callable(v)]


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
@pytest.mark.parametrize("name", list_indicators())
def test_indicator(name):
    func = getattr(indicators, name)
    kwds = sample_params(func)
    indicator = func(**kwds)
    prices = sample_prices()
    result = indicator(prices)
    assert result is not None


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_indicator_pipe_composition():
    chain = EMA(20) | ROC(1)
    assert isinstance(chain, IndicatorChain)
    assert repr(chain) == "EMA(20) | ROC(1)"
    prices = sample_prices()
    result = chain(prices)
    assert result is not None


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_prices_pipe_indicator():
    prices = sample_prices()
    result = prices | SMA(20)
    assert result is not None


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_prices_pipe_chain():
    prices = sample_prices()
    result = prices | EMA(20) | ROC(1)
    assert result is not None


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_matmul_deprecation():
    prices = sample_prices()
    with pytest.warns(DeprecationWarning):
        SMA(20) @ prices
    with pytest.warns(DeprecationWarning):
        ROC(1) @ EMA(20)


@pytest.mark.skipif(not has_polars, reason="requires polars")
def test_indicator_rejects_polars():
    prices = sample_prices(backend="polars")
    with pytest.raises(TypeError, match="mintalib.expressions"):
        SMA(20)(prices)


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_eval_indicator():
    from mintalib.indicators import EVAL

    prices = sample_prices()
    result = EVAL("close > 0")(prices)
    assert result.shape == (len(prices),)
    assert result.dtype == "float64"
    assert (result == 1.0).all()

    flag = EVAL("close - close.shift(1)", as_flag=True)(prices)
    assert set(flag.dropna().unique()) <= {0.0, 1.0}


@pytest.mark.skipif(not has_polars, reason="requires polars")
def test_eval_rejects_polars():
    from mintalib.indicators import EVAL

    prices = sample_prices(backend="polars")
    with pytest.raises(TypeError, match="mintalib.expressions"):
        EVAL("close > 0")(prices)
