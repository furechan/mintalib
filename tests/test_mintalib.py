import pytest

from mintalib import core, indicators
from mintalib.samples import sample_prices
from mintalib.testing import first_param, sample_params


try:
    import pandas
except ImportError:
    pandas = None

try:
    import polars
except ImportError:
    polars = None


def core_functions():
    return [
        k for k, v in vars(core).items()
        if k.startswith(("calc_", "flag_"))
        and callable(v)
        and first_param(v) in ("prices", "series")
    ]


def list_indicators():
    return [k for k, v in vars(indicators).items() if k.isupper() and callable(v)]



def test_samples():
    prices = sample_prices()
    assert prices is not None


@pytest.mark.parametrize("name", core_functions())
def test_core(name):
    func = getattr(core, name)

    ftype = first_param(func)
    assert ftype in ("series", "prices")

    kwds = sample_params(func)

    data = sample_prices()

    if ftype == "series":
        data = data['close']

    result = func(data, **kwds)
    assert result is not None


@pytest.mark.skipif(pandas is None, reason="requires pandas")
@pytest.mark.parametrize("name", list_indicators())
def test_indicator(name):
    func = getattr(indicators, name)
    kwds = sample_params(func)
    indicator = func(**kwds)

    assert callable(func)

    prices = sample_prices()

    result = indicator(prices)
    assert result is not None

