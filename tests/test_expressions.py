import pytest

pl = pytest.importorskip("polars")

from mintalib import expressions  # noqa: E402
from mintalib.samples import sample_prices  # noqa: E402
from mintalib.testing import sample_params  # noqa: E402


def list_expressions():
    return [k for k, v in vars(expressions).items() if k.isupper() and callable(v)]


@pytest.fixture(scope="module")
def prices():
    return sample_prices(backend="polars")


@pytest.mark.parametrize("name", list_expressions())
def test_expression(name, prices):
    func = getattr(expressions, name)
    kwds = sample_params(func)
    expr = func(**kwds)
    if isinstance(expr, tuple):
        result = prices.select(*expr)
    else:
        result = prices.select(expr)
    assert result is not None
    assert len(result) > 0
