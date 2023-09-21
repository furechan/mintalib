import unittest

import json

from pathlib import Path

from mintalib import opers, utils


DATA_FILE = "../../tests/data/test_opers.json"


def load_test_data():
    folder = Path(__file__).parent
    file = folder / DATA_FILE
    return json.loads(file.read_text())


def create_test(name: str, **kwargs):
    params = [f"{k}={v!r}" for k, v in kwargs.items()]
    description = name + "(" + ", ".join(params) + ")"

    def test_oper():
        klass = getattr(opers, name)
        data = utils.sample_prices()
        func = klass(**kwargs)
        result = func(data)
        assert result is not None

    return unittest.FunctionTestCase(test_oper, description=description)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    data = load_test_data()
    for kwds in data:
        test = create_test(**kwds)
        suite.addTest(test)
    return suite
