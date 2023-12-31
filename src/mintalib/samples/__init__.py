""" data samples """

import numpy as np
import pandas as pd
import datetime as dt

from pathlib import Path

FOLDER = Path(__file__).parent


def sample_prices(item: str = None):
    """Sample prices dataframe or series

    Args:
        item (optional) : use as column name to return a series

    Returns:
        A prices dataframe or a series if item is specified
    """

    file = FOLDER.joinpath("sample-prices.csv")

    prices = pd.read_csv(file, index_col=0, parse_dates=True)

    if item is not None:
        return prices[item]

    return prices


def load_prices(target: str = None):
    """Load sample prices in target format

    Args:
        target (None | 'pandas` | 'polars') : target dataframe format

    Returns:
        A numpy structured array or a dataframe of specified target
    """

    if target not in (None, "pandas", "polars"):
        raise ValueError(f"Invalid target {target!r}")

    file = FOLDER.joinpath("sample-prices.csv")

    prices = np.genfromtxt(
        file,
        delimiter=",",
        converters={0: dt.datetime.fromisoformat},
        dtype=None,
        names=True,
        encoding="utf-8",
    )

    if target == "pandas":
        import pandas

        prices = pandas.DataFrame(prices).set_index("date")

    elif target == "polars":
        import polars

        prices = polars.DataFrame(prices)

    return prices
