import pytest

import numpy as np
import pandas as pd

from mintalib import functions

from mintalib.utils import random_walk, sample_prices


def test_functions():
    assert functions is not None


@pytest.mark.parametrize(
    "name, arg1, arg2",
    [("ema", 10, None), ("ema", 20, 0), ("sma", 10, 20)]
)
def test_function(name, arg1, arg2):
    func = getattr(functions, name)
    assert func is not None


TEMPLATE = """
def test_{name}():
    series = random_walk(500)
    result = functions.{name}(series)
    assert isinstance(result, pd.Series)
"""

# names = [n[3:] for n in dir(numeric) if n.startswith("np_")]
names = ("ema", )

for name in names:
    exec(TEMPLATE.format(name=name))
