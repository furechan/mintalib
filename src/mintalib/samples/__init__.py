"""Sample prices data"""

from functools import lru_cache
from importlib import resources


TIMEZONE = "America/New_York"
FREQUENCIES = "daily", "hourly", "minute"


@lru_cache
def sample_prices(freq: str = "daily", *, backend: str = "pandas"):
    """Load bundled sample OHLCV prices for testing and examples.

    Results are cached after the first call (per unique combination of arguments).

    Args:
        freq: Data frequency — ``"daily"``, ``"hourly"``, or ``"minute"``.
        backend: Target DataFrame backend — ``"pandas"`` or ``"polars"``.
            The backend module is imported lazily so the unused one is not required.

    Returns:
        DataFrame with OHLCV columns and a datetime index (pandas) or datetime column (polars).
    """

    if freq not in FREQUENCIES:
        raise ValueError(f"Invalid freq {freq!r}")

    fname = f"{freq}-prices.csv"
    path = resources.files(__name__).joinpath(fname)

    match backend:
        case "pandas":
            return _load_pandas(path)
        case "polars":
            return _load_polars(path, freq=freq)
        case _:
            raise ValueError(f"Unknown backend {backend!r}")


def _load_pandas(path):
    import pandas as pd
    from pandas.api.types import is_object_dtype

    with path.open("r") as file:
        prices = pd.read_csv(file, index_col=0, parse_dates=True)

    if is_object_dtype(prices.index):
        prices.index = pd.to_datetime(prices.index, utc=True).tz_convert(TIMEZONE)

    return prices


def _load_polars(path, *, freq: str):
    import polars as pl

    with path.open("rb") as file:
        prices = pl.read_csv(file, try_parse_dates=True)

    col = prices.columns[0]  # "date" (daily) or "datetime" (hourly/minute)

    if freq != "daily":
        tz = getattr(prices.schema[col], "time_zone", None)
        if tz is None:
            prices = prices.with_columns(
                pl.col(col).dt.replace_time_zone("UTC").dt.convert_time_zone(TIMEZONE)
            )
        else:
            prices = prices.with_columns(pl.col(col).dt.convert_time_zone(TIMEZONE))

    return prices
