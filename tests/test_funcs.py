import unittest

from mintalib import funcs, utils

from mintalib.helper import func_type, sample_params


def list_funcs():
    return [
        v for k, v in vars(funcs).items()
        if k.isupper() and callable(v)
    ]


def create_test(func):
    name = func.__name__

    ftype = func_type(func)
    if ftype not in ('series', 'prices'):
        return None

    try:
        kwds = sample_params(func)
    except NameError:
        return None

    item = 'close' if ftype == 'series' else None

    args = [item if item else 'prices']
    args += [f"{k}={v!r}" for k, v in kwds.items()]
    description = name + "(" + ", ".join(args) + ")"

    def test_func():
        data = utils.sample_prices(item)
        result = func(data, **kwds)
        assert result is not None

    return unittest.FunctionTestCase(test_func, description=description)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    funcs = list_funcs()
    for func in funcs:
        test = create_test(func)
        if test is not None:
            suite.addTest(test)
    return suite
