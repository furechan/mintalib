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
def test_then_chains_indicators():
    chain = EMA(20).then(ROC(1))
    assert isinstance(chain, IndicatorChain)
    assert repr(chain) == repr(EMA(20) | ROC(1))


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_then_rejects_non_indicator():
    with pytest.raises(TypeError, match=r"\.then\(\)"):
        EMA(20).then("not an indicator")


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
def test_pipe_rejects_invalid_left():
    with pytest.raises(TypeError, match="DataFrame or Series"):
        "not data" | SMA(20)


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_indicator_output_names():
    from mintalib.indicators import MACD

    assert SMA(20).output_names is None
    assert MACD().output_names == ("macd", "macdsignal", "macdhist")
    assert (EMA(20) | ROC(1)).output_names is None
    assert (EMA(20) | MACD()).output_names == ("macd", "macdsignal", "macdhist")


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_as_expr_single_output():
    from pandas.api.typing import Expression

    expr = SMA(20).as_expr()
    assert isinstance(expr, Expression)

    prices = sample_prices()
    result = prices.assign(sma=expr)
    assert "sma" in result.columns
    assert result["sma"].notna().any()


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_then_fluent_with_as_expr():
    from pandas.api.typing import Expression

    expr = EMA(20).then(ROC(1)).as_expr()
    assert isinstance(expr, Expression)


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_as_expr_rejects_multi_output():
    from mintalib.indicators import MACD

    with pytest.raises(TypeError, match="multiple outputs"):
        MACD().as_expr()


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
