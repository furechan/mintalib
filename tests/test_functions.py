import pytest

from pytest import mark, fixture

from mintalib import testing


@fixture(params=[20])
def period(request):
    return request.param


@fixture(params=['close', 'change', 'change'])
def item(request):
    return request.param


def test_avgprice():
    assert testing.test_function('avgprice')


def test_typprice():
    assert testing.test_function('typprice')


def test_wclprice():
    assert testing.test_function('wclprice')


def test_midprice():
    assert testing.test_function('midprice')


def test_trange():
    assert testing.test_function('trange')


@mark.parametrize("period", [1])
@mark.parametrize("item", ['close'])
def test_roc(item, period):
    assert testing.test_function('roc', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_min(item, period):
    assert testing.test_function('min', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_max(item, period):
    assert testing.test_function('max', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_ema(item, period):
    assert testing.test_function('ema', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_sma(item, period):
    assert testing.test_function('sma', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_wma(item, period):
    assert testing.test_function('wma', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_dema(item, period):
    assert testing.test_function('dema', period, item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close', 'change', 'volume'])
def test_tema(item, period):
    assert testing.test_function('tema', period, item=item)


@mark.parametrize("period", [14])
@mark.parametrize("item", ['close'])
def test_rsi(item, period):
    assert testing.test_function('rsi', period)


@mark.parametrize("period", [14])
def test_atr(period):
    assert testing.test_function('atr', period)


@mark.parametrize("period", [14])
def test_adx(period):
    assert testing.test_function('adx', period)


@mark.parametrize("item", ['close'])
def test_macd(item):
    assert testing.test_function('macd', item=item)


@mark.parametrize("item", ['close'])
def test_ppo(item):
    assert testing.test_function('ppo', item=item)


@mark.parametrize("period", [20])
@mark.parametrize("item", ['close'])
def test_slope(item, period):
    assert testing.test_function('slope', period, item=item)
