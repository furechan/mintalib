import pytest

from mintalib import core
from mintalib.samples import sample_prices
from mintalib.testing import first_param, sample_params

from importlib.util import find_spec

has_pandas = find_spec("pandas") is not None
has_polars = find_spec("polars") is not None


def list_core_functions():
    return [
        k for k, v in vars(core).items()
        if k.startswith(("calc_", "flag_"))
        and callable(v)
        and first_param(v) in ("prices", "series")
    ]


@pytest.fixture(params=[
    pytest.param("pandas", marks=pytest.mark.skipif(not has_pandas, reason="requires pandas")),
    pytest.param("polars", marks=pytest.mark.skipif(not has_polars, reason="requires polars")),
])
def prices(request):
    return sample_prices(backend=request.param)


@pytest.mark.parametrize("name", list_core_functions())
def test_core(name, prices):
    func = getattr(core, name)
    ftype = first_param(func)
    kwds = sample_params(func)
    data = prices
    if ftype == "series":
        data = data["close"]
    result = func(data, **kwds)
    assert result is not None
