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
