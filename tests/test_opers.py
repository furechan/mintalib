import unittest

from mintalib import opers, utils

from mintalib.helper import sample_params


def list_opers():
    return [
        v for k, v in vars(opers).items()
        if k.isupper() and isinstance(v, type)
    ]


def create_test(cls):
    name = cls.__name__

    try:
        kwds = sample_params(cls)
    except NameError:
        return None

    args = [f"{k}={v!r}" for k, v in kwds.items()]
    description = name + "(" + ", ".join(args) + ")"

    def test_oper():
        data = utils.sample_prices()
        func = cls(**kwds)
        result = func(data)
        assert result is not None

    return unittest.FunctionTestCase(test_oper, description=description)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    opers = list_opers()
    for cls in opers:
        test = create_test(cls)
        if test is not None:
            suite.addTest(test)
    return suite
