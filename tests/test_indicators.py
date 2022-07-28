import pytest

import numpy as np
import pandas as pd

from mintalib import indicators

from mintalib.utils import random_walk, sample_prices


def test_numeric():
    assert indicators is not None


TEMPLATE = """
def test_{name}():
    series = random_walk(500)
    indicator = indicators.{name}() 
    result = indicator(series)
    assert isinstance(result, pd.Series)
"""

# names = [n[3:] for n in dir(numeric) if n.startswith("np_")]
names = ("EMA", )

for name in names:
    exec(TEMPLATE.format(name=name))
