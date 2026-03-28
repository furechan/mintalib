import pytest

from mintalib import indicators
from mintalib.samples import sample_prices
from mintalib.testing import sample_params

pandas = None
try:
    import pandas
except ImportError:
    pass


def list_indicators():
    return [k for k, v in vars(indicators).items() if k.isupper() and callable(v)]


@pytest.mark.skipif(pandas is None, reason="requires pandas")
@pytest.mark.parametrize("name", list_indicators())
def test_indicator(name):
    func = getattr(indicators, name)
    kwds = sample_params(func)
    indicator = func(**kwds)
    prices = sample_prices()
    result = indicator(prices)
    assert result is not None
