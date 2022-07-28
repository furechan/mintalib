import pytest

import numpy as np
import pandas as pd

from mintalib import core

from mintalib.utils import random_walk, sample_prices

def test_core():
    assert core is not None

TEMPLATE = """
def test_{name}():
    series = random_walk(500)
    result = core.calc_{name}(series)
    assert isinstance(result, pd.Series)
"""

# names = [n[3:] for n in dir(numeric) if n.startswith("np_")]
names = ("ema", "sma", "rma", "rsi")

for name in names:
    exec(TEMPLATE.format(name=name))
