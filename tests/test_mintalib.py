import pytest

from mintalib import core, functions, indicators
from mintalib.samples import sample_prices
from mintalib.testing import first_param, sample_params

try:
    import polars
    from mintalib import expressions
except ImportError:
    polars = expressions = None


def core_functions():
    return [
        k for k, v in vars(core).items()
        if k.startswith(("calc_", "flag_"))
        and callable(v)
        and first_param(v) in ("prices", "series")
    ]

def list_functions():
    return [k for k, v in vars(functions).items() if callable(v) and first_param(v) in ("prices", "series")]

def list_indicators():
    return [k for k, v in vars(indicators).items() if k.isupper() and callable(v)]

def list_expressions():
    if expressions is not None:
        return [k for k, v in vars(expressions).items() if k.isupper() and callable(v)]
    return ()



def test_samples():
    prices = sample_prices()
    assert prices is not None


@pytest.mark.parametrize("name", core_functions())
def test_core(name):
    func = getattr(core, name)

    ftype = first_param(func)
    assert ftype in ("series", "prices")

    kwds = sample_params(func)

    item = "close" if ftype == "series" else None
    data = sample_prices(item=item)

    result = func(data, **kwds)
    assert result is not None


@pytest.mark.parametrize("name", list_functions())
def test_function(name):
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
    func = getattr(indicators, name)
    kwds = sample_params(func)
    indicator = func(**kwds)

    assert callable(func)

    prices = sample_prices()

    result = indicator(prices)
    assert result is not None


@pytest.mark.skipif(polars is None, reason="requires polars")
@pytest.mark.parametrize("name", list_expressions())
def test_expression(name):
    func = getattr(expressions, name)
    kwds = sample_params(func)
    expr = func(**kwds)

    prices = sample_prices()
    prices = polars.from_pandas(prices, include_index=True)

    result = prices.select(expr)

    assert result is not None
