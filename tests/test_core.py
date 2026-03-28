import pytest

from mintalib import core
from mintalib.samples import sample_prices
from mintalib.testing import first_param, sample_params


def list_core_functions():
    return [
        k for k, v in vars(core).items()
        if k.startswith(("calc_", "flag_"))
        and callable(v)
        and first_param(v) in ("prices", "series")
    ]


@pytest.mark.parametrize("name", list_core_functions())
def test_core(name):
    func = getattr(core, name)
    ftype = first_param(func)
    kwds = sample_params(func)
    data = sample_prices()
    if ftype == "series":
        data = data["close"]
    result = func(data, **kwds)
    assert result is not None
