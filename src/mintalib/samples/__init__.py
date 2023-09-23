""" data samples """

import numpy as np
import datetime as dt

from pathlib import Path

FOLDER = Path(__file__).parent


def sample_prices(item: str = None, *, target: str = None):
    """Sample prices dataframe or series

    Args:
        item (optional) : use as column name to return a series
        target (None | 'pandas` | 'polars') : target dataframe format

    Returns:
        A numpy structured array or a dataframe of specified target
        If item is specified will return corresponding column
    """

    if target not in (None, 'pandas', 'polars'):
        raise ValueError(f"Invalid target {target!r}")

    file = FOLDER.joinpath("sample-prices.csv")

    prices = np.genfromtxt(
        file, delimiter=',',
        converters={0: dt.datetime.fromisoformat},
        dtype=None, names=True,
        encoding='utf-8'
    )

    if target == 'pandas':
        import pandas
        prices = pandas.DataFrame(prices).set_index('date')

    elif target == 'polars':
        import polars
        prices = polars.DataFrame(prices)

    if item is not None:
        return prices[item]

    return prices
