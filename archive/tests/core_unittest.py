import unittest

import json

from pathlib import Path

from mintalib import core, utils

folder = Path(__file__).parent

DATA_FILE = "../../tests/core_tests.json"

def get_core_func(name):
    fname = f"calc_{name.lower()}"
    return getattr(core, fname)


def load_test_data():
    file = folder / DATA_FILE
    return json.loads(file.read_text())


class CoreTest(unittest.TestCase):
    __test__ = False

    def __init__(self, name: str=None, *args, item: str = None, **kwargs):
        super().__init__()
        self.name = name
        self.args = args
        self.item = item
        self.kwargs = kwargs

    @classmethod
    def from_json(cls, data):
        name = data.get('name')
        args = data.get('args', ())
        item = data.get('item')
        kwargs = data.get('kwargs', {})
        return cls(name, *args, item=item, **kwargs)

    def shortDescription(self):
        params = [self.item if self.item else 'prices']
        params += [repr(arg) for arg in self.args]
        params += [f"{k}={v!r}" for k, v in self.kwargs.items()]
        return self.name + "(" + ", ".join(params) + ")"

    def runTest(self):
        if self.name is None:
            return
        func = get_core_func(self.name)
        series = utils.sample_series(self.item)
        result = func(series, *self.args, **self.kwargs)
        self.assertIsNotNone(result)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    # suite.addTest(FunctionTest('EMA', 5, item='close'))
    data = load_test_data()
    for rec in data:
        test = CoreTest.from_json(rec)
        suite.addTest(test)
    return suite
