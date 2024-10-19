import pytest

from mintalib import core, functions, indicators
from mintalib.samples import sample_prices
from mintalib.testing import first_param, sample_params


def list_calcs():
    return [
        k
        for k, v in vars(core).items()
        if k.startswith(("calc_", "flag_"))
        and callable(v)
        and first_param(v) in ("prices", "series")
    ]


def list_functions():
    return [k for k, v in vars(functions).items() if k.isupper() and callable(v)]


def list_indicators():
    return [k for k, v in vars(indicators).items() if k.isupper() and callable(v)]


def test_samples():
    prices = sample_prices()
    assert prices is not None


@pytest.mark.parametrize("name", list_calcs())
def test_calc(name):
    print("test_calc", name)

    func = getattr(core, name)

    ftype = first_param(func)
    assert ftype in ("series", "prices")

    kwds = sample_params(func)

    item = "close" if ftype == "series" else None
    data = sample_prices(item=item)

    result = func(data, **kwds)
    assert result is not None


@pytest.mark.parametrize("name", list_functions())
def test_funct(name):
    print("test_func", name)

    func = getattr(functions, name)

    ftype = first_param(func)
    assert ftype in ("series", "prices")

    kwds = sample_params(func)

    item = "close" if ftype == "series" else None
    data = sample_prices(item=item)

    result = func(data, **kwds)
    assert result is not None


@pytest.mark.parametrize("name", list_indicators())
def test_indicator(name):
    print("test_indicator", name)

    klass = getattr(indicators, name)
    kwds = sample_params(klass)
    func = klass(**kwds)

    assert callable(func)

    data = sample_prices()

    result = func(data)
    assert result is not None
