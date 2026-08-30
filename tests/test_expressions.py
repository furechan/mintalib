import inspect
from typing import Any, Callable

import pytest

pl = pytest.importorskip("polars")

from mintalib import expressions  # noqa: E402
from mintalib import core  # noqa: E402
from mintalib.model import expression as expression_model  # noqa: E402
from mintalib.samples import sample_prices  # noqa: E402
from mintalib.testing import sample_params  # noqa: E402


def list_expressions():
    return [k for k, v in vars(expressions).items() if k.isupper() and callable(v)]


def call_untyped(func: Callable[..., Any], *args, **kwargs):
    return func(*args, **kwargs)


@pytest.fixture(scope="module")
def prices():
    return sample_prices(backend="polars")


@pytest.mark.parametrize("name", list_expressions())
def test_expression(name, prices):
    func = getattr(expressions, name)
    kwds = sample_params(func)
    expr = func(**kwds)
    result = prices.select(expr)
    assert result is not None
    assert len(result) > 0


def price_expressions():
    return [
        name
        for name in list_expressions()
        if getattr(getattr(core, f"calc_{name.lower()}"), "metadata", {}).get(
            "inputs"
        )
    ]


@pytest.mark.parametrize("name", price_expressions())
def test_price_expression_signature(name):
    func = getattr(expressions, name)
    calc_func = getattr(core, f"calc_{name.lower()}")
    inputs = calc_func.metadata["inputs"]
    params = inspect.signature(func).parameters

    assert "src" not in params
    for input_name in inputs:
        assert params[input_name].kind == inspect.Parameter.KEYWORD_ONLY
        assert params[input_name].default == input_name


def test_price_expression_accepts_named_sources(prices):
    renamed = prices.with_columns(
        pl.col("high").alias("h"),
        pl.col("low").alias("l"),
        pl.col("close").alias("c"),
    )

    expected = prices.select(expressions.ATR(20)).to_series()
    result = renamed.select(
        expressions.ATR(20, high="h", low="l", close="c")
    ).to_series()

    assert result.equals(expected, null_equal=True)


def test_obv_expression(prices):
    expected = core.calc_obv(prices["close"], prices["volume"])

    result = prices.select(expressions.OBV()).to_series()

    assert result.name == "obv"
    assert result.to_numpy() == pytest.approx(expected, nan_ok=True)


def test_obv_expression_accepts_named_sources(prices):
    renamed = prices.with_columns(
        pl.col("close").alias("settle"),
        pl.col("volume").alias("size"),
    )

    expected = prices.select(expressions.OBV()).to_series()
    result = renamed.select(
        expressions.OBV(close=pl.col("settle"), volume="size")
    ).to_series()

    assert result.equals(expected, null_equal=True)


def test_obv_expression_rejects_src():
    with pytest.raises(TypeError):
        call_untyped(expressions.OBV, src="close")


def test_price_expression_rejects_src():
    with pytest.raises(TypeError):
        call_untyped(expressions.ATR, src="prices")


def test_series_expression_has_explicit_close_default():
    src = inspect.signature(expressions.SMA).parameters["src"]

    assert src.annotation == expressions.IntoExpr
    assert src.default == "close"


def test_expression_primitives_are_reexported_from_model():
    assert expressions.IntoExpr is expression_model.IntoExpr
    assert expressions.CLOSE is expression_model.CLOSE
    assert expressions.OHLC is expression_model.OHLC


def test_series_expression_rejects_none_source():
    with pytest.raises(ValueError, match="src must be a string or a Polars expression"):
        call_untyped(expressions.SMA, 20, src=None)


def test_series_expression_accepts_positional_source(prices):
    expected = prices.select(expressions.SMA(20)).to_series()
    result = prices.select(
        pl.col("close").pipe(expressions.SMA, period=20)
    ).to_series()

    assert result.equals(expected, null_equal=True)
