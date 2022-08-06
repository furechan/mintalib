import pytest

from pytest import mark, fixture

from mintalib import testing


@fixture(params=[20])
def period(request):
    return request.param


@fixture(params=['close', 'change', 'change'])
def item(request):
    return request.param


@mark.parametrize("period", [1])
@mark.parametrize("item", ['close'])
def test_roc(item, period):
    assert testing.test_function('roc', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close'])
def test_ema(item, period):
    assert testing.test_function('ema', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close'])
def test_sma(item, period):
    assert testing.test_function('sma', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close'])
def test_wma(item, period):
    assert testing.test_function('wma', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close'])
def test_dema(item, period):
    assert testing.test_function('dema', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close'])
def test_tema(item, period):
    assert testing.test_function('tema', period, item=item)


@mark.parametrize("item", ['close'])
def test_macd(item):
    assert testing.test_function('macd', item=item)


@mark.parametrize("period", [14])
def test_atr(period):
    assert testing.test_function('atr', period)


@mark.parametrize("period", [14])
def test_adx(period):
    assert testing.test_function('adx', period)
