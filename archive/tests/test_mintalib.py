from pytest import mark, fixture

import json
import numpy as np

from pathlib import Path

from mintalib import core
from mintalib import utils

folder = Path(__file__).parent


def get_core_func(name):
    fname = f"calc_{name.lower()}"
    return getattr(core, fname)

def pytest_generate_tests(metafunc):
    params = metafunc.fixturenames
    print("generating tests for ", metafunc, params)
    file = folder / "_tests.json"
    data = json.loads(file.read_text())
    data = [ [r.get(k) for k in params ] for r in data]
    metafunc.parametrize(",".join(params), data)


#@mark.parametrize("item", ['close', 'change', 'volume'])
#@mark.parametrize("args", [(5, )])
#@mark.parametrize("name", ['EMA', 'SMA'])

def test_core(name: str, args: tuple, item: str):
    func = get_core_func(name)
    series = utils.sample_series(item)
    result = func(series, *args)
    assert result is not None
