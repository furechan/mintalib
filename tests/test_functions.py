import inspect
from typing import Any, Callable

import numpy as np
import pytest

from mintalib import core, functions
from mintalib.model.function import wrap_columns_function
from mintalib.samples import sample_prices
from mintalib.testing import first_param, sample_params

from importlib.util import find_spec

has_pandas = find_spec("pandas") is not None


def call_untyped(func: Callable[..., Any], *args, **kwargs):
    """Exercise runtime validation with intentionally invalid arguments."""

    return func(*args, **kwargs)


def list_functions():
    return [
        k for k, v in vars(functions).items()
        if k.islower()
        and callable(v)
        and not k.startswith("_")
        and v.__module__ == functions.__name__
    ]


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
@pytest.mark.parametrize("name", list_functions())
def test_function(name):
    func = getattr(functions, name)
    calc_func = getattr(core, f"calc_{name}")
    ftype = first_param(calc_func)
    inputs = getattr(calc_func, "metadata", {}).get("inputs") or ()
    kwds = sample_params(calc_func)
    data = sample_prices()
    if ftype == "series":
        data = data["close"]
        result = func(data, **kwds)
    else:
        result = func(*(data[column] for column in inputs), **kwds)
    assert result is not None


def price_functions():
    return [
        name
        for name in list_functions()
        if getattr(getattr(core, f"calc_{name}"), "metadata", {}).get("inputs")
    ]


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
@pytest.mark.parametrize("name", price_functions())
def test_prices_function_accepts_columns(name):
    func = getattr(functions, name)
    calc_func = getattr(core, f"calc_{name}")
    inputs = calc_func.metadata["inputs"]
    prices = sample_prices()

    assert tuple(inspect.signature(func).parameters)[: len(inputs)] == inputs
    parameters = tuple(inspect.signature(func).parameters.values())
    assert all(
        parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        for parameter in parameters[len(inputs):]
    )

    expected = calc_func(
        *(prices[column] for column in inputs),
        **sample_params(calc_func),
    )
    result = func(*(prices[column] for column in inputs), **sample_params(calc_func))

    if hasattr(expected, "_fields"):
        np.testing.assert_allclose(
            result.to_numpy(),
            np.column_stack(expected),
            equal_nan=True,
        )
    elif hasattr(expected, "columns"):
        assert result.equals(expected)
    else:
        assert np.allclose(result, expected, equal_nan=True)


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_obv_preserves_close_index():
    prices = sample_prices()

    result = functions.obv(prices["close"], prices["volume"])
    expected = core.calc_obv(prices["close"], prices["volume"])

    assert result.index.equals(prices.index)
    np.testing.assert_allclose(result, expected, equal_nan=True)


def test_obv_accepts_numpy_columns_and_keywords():
    close = np.array([10.0, 11.0, 9.0])
    volume = np.array([100.0, 20.0, 30.0])

    result = functions.obv(close=close, volume=volume)

    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, [100.0, 120.0, 90.0])


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_prices_function_accepts_keyword_columns():
    prices = sample_prices()

    expected = core.calc_atr(
        prices["high"],
        prices["low"],
        prices["close"],
    )
    result = functions.atr(
        high=prices["high"],
        low=prices["low"],
        close=prices["close"],
    )

    np.testing.assert_allclose(result, expected, equal_nan=True)


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_prices_function_accepts_positional_parameters():
    prices = sample_prices()

    expected = core.calc_atr(
        prices["high"],
        prices["low"],
        prices["close"],
        20,
    )
    result = functions.atr(
        prices["high"],
        prices["low"],
        prices["close"],
        20,
    )

    np.testing.assert_allclose(result, expected, equal_nan=True)

def test_function_wrapper_accepts_columnar_kernel():
    def calc_columnar(close, volume, period=1):
        return np.asarray(close) + np.asarray(volume) * period

    setattr(calc_columnar, "metadata", {"inputs": ("close", "volume")})

    @wrap_columns_function(calc_columnar)
    def columnar(close, volume, *, period=1): ...

    close = np.array([1.0, 2.0])
    volume = np.array([3.0, 4.0])

    np.testing.assert_array_equal(columnar(close, volume, period=2), [7.0, 10.0])

    with pytest.raises(TypeError, match="too many positional arguments"):
        call_untyped(columnar, close, volume, 2)


def test_function_wrapper_rejects_missing_inputs_metadata():
    def calc_invalid(close, volume):
        return np.asarray(close) + np.asarray(volume)

    with pytest.raises(ValueError, match="Missing inputs metadata for 'calc_invalid'"):
        wrap_columns_function(calc_invalid)


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_prices_function_rejects_incomplete_columns():

    prices = sample_prices()

    with pytest.raises(TypeError, match="missing a required argument: 'low'"):
        call_untyped(functions.atr, prices["close"])

    with pytest.raises(TypeError, match="missing a required argument: 'low'"):
        call_untyped(functions.atr, np.asarray(prices["close"]))

    with pytest.raises(TypeError):
        call_untyped(functions.atr, prices=prices)


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_series_function_rejects_prices():
    prices = sample_prices()

    with pytest.raises(TypeError, match="wrong shape"):
        functions.sma(prices, 20)

    with pytest.raises(TypeError, match="Expected a series"):
        functions.sma({"close": [1.0, 2.0, 3.0]}, 20)


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_series_function_accepts_series():
    prices = sample_prices()

    assert functions.sma(prices["close"], 20) is not None
    assert functions.sma(np.asarray(prices["close"]), 20) is not None
