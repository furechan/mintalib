import pytest

from mintalib import functions
from mintalib.samples import sample_prices
from mintalib.testing import first_param, sample_params

from importlib.util import find_spec

has_pandas = find_spec("pandas") is not None


def list_functions():
    return [
        k for k, v in vars(functions).items()
        if k.islower()
        and callable(v)
        and not k.startswith("_")
        and first_param(v) in ("prices", "series")
    ]


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
@pytest.mark.parametrize("name", list_functions())
def test_function(name):
    func = getattr(functions, name)
    ftype = first_param(func)
    kwds = sample_params(func)
    data = sample_prices()
    if ftype == "series":
        data = data["close"]
    result = func(data, **kwds)
    assert result is not None


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_prices_function_rejects_series():
    import numpy as np

    prices = sample_prices()

    with pytest.raises(TypeError, match="Expected a prices data frame"):
        functions.atr(prices["close"])

    with pytest.raises(TypeError, match="named fields"):
        functions.atr(np.asarray(prices["close"]))


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_series_function_rejects_prices():
    prices = sample_prices()

    with pytest.raises(TypeError, match="wrong shape"):
        functions.sma(prices, 20)

    with pytest.raises(TypeError, match="Expected a series"):
        functions.sma({"close": [1.0, 2.0, 3.0]}, 20)


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_series_function_accepts_series():
    import numpy as np

    prices = sample_prices()

    assert functions.sma(prices["close"], 20) is not None
    assert functions.sma(np.asarray(prices["close"]), 20) is not None


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_price_item_kwarg():
    import numpy as np

    prices = sample_prices()

    result = functions.price(prices, item="high")
    assert np.allclose(result, prices["high"], equal_nan=True)
