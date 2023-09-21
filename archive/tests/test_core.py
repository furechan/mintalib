import unittest

import json

from pathlib import Path

from mintalib import core, utils


DATA_FILE = "../../tests/data/test_core.json"


def load_test_data():
    folder = Path(__file__).parent
    file = folder / DATA_FILE
    return json.loads(file.read_text())


def create_test(name: str, item: str = None, **kwargs):
    params = [item if item else 'prices']
    params += [f"{k}={v!r}" for k, v in kwargs.items()]
    description = name + "(" + ", ".join(params) + ")"

    def test_core():
        func = getattr(core, name)
        data = utils.sample_prices(item)
        result = func(data, **kwargs)
        assert result is not None

    return unittest.FunctionTestCase(test_core, description=description)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    data = load_test_data()
    for kwds in data:
        test = create_test(**kwds)
        suite.addTest(test)
    return suite
