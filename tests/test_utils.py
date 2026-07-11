import pytest

import numpy as np

from mintalib.utils import normalize_prices

from importlib.util import find_spec

has_pandas = find_spec("pandas") is not None
has_polars = find_spec("polars") is not None


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_normalize_prices_pandas():
    import pandas as pd

    prices = pd.DataFrame(
        {"Open": [1.0], "High": [2.0], "Low": [0.5], "Close": [1.5], "Volume": [100.0]},
        index=pd.Index([pd.Timestamp("2026-01-02")], name="Date"),
    )

    result = normalize_prices(prices)

    assert list(result.columns) == ["open", "high", "low", "close", "volume"]
    assert result.index.name == "date"
    # original left unchanged
    assert list(prices.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert prices.index.name == "Date"

    # unnamed index does not break
    result = normalize_prices(pd.DataFrame({"Close": [1.0]}))
    assert list(result.columns) == ["close"]
    assert result.index.name is None


@pytest.mark.skipif(not has_polars, reason="requires polars")
def test_normalize_prices_polars():
    import polars as pl

    prices = pl.DataFrame(
        {"Open": [1.0], "High": [2.0], "Low": [0.5], "Close": [1.5], "Volume": [100.0]}
    )

    result = normalize_prices(prices)

    assert result.columns == ["open", "high", "low", "close", "volume"]
    assert prices.columns == ["Open", "High", "Low", "Close", "Volume"]


@pytest.mark.skipif(not has_pandas, reason="requires pandas")
def test_normalize_prices_rejects_other():
    import pandas as pd

    with pytest.raises(TypeError, match="pandas or polars dataframe"):
        normalize_prices({"Close": [1.0]})

    with pytest.raises(TypeError, match="pandas or polars dataframe"):
        normalize_prices(np.arange(5.0))

    with pytest.raises(TypeError, match="pandas or polars dataframe"):
        normalize_prices(pd.Series([1.0]))
