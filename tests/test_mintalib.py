import pytest

from mintalib import core, opers, utils

from mintalib.helper import func_type, sample_params


def list_funcs():
    return [
        k for k, v in vars(core).items()
        if k.isupper() and callable(v)
    ]


def list_opers():
    return [
        k for k, v in vars(opers).items()
        if k.isupper() and callable(v)
    ]


@pytest.mark.parametrize("name", list_funcs())
def test_func(name):
    print("test_func", name)

    func = getattr(core, name)

    ftype = func_type(func)
    assert ftype in ('series', 'prices')

    kwds = sample_params(func)

    item = 'close' if ftype == 'series' else None
    data = utils.sample_prices(item)

    result = func(data, **kwds)
    assert result is not None


@pytest.mark.parametrize("name", list_opers())
def test_oper(name):
    print("test_oper", name)

    klass = getattr(opers, name)
    kwds = sample_params(klass)
    func = klass(**kwds)

    assert callable(func)

    data = utils.sample_prices()

    result = func(data)
    assert result is not None

