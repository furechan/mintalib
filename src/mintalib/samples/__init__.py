"""Sample prices data"""

from functools import lru_cache
from importlib import resources


TIMEZONE = "America/New_York"
FREQUENCIES = "daily", "hourly", "minute"
SAMPLE_TICKERS = tuple(f"T{i:03d}" for i in range(1, 501))


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


@lru_cache
def sample_dataset(
    n_tickers: int = 500,
    *,
    freq: str = "daily",
    max_bars: int = 0,
):
    """Synthetic multi-ticker polars dataset for benchmarking `.over()` expressions.

    Stacks ``n_tickers`` copies of :func:`sample_prices` (polars backend) with a
    synthetic ``ticker`` column (``"T001"`` … ``"T500"``), sorted by
    ``(ticker, date)`` so it is ready for ``.over("ticker")`` use.

    Results are cached after the first call (per unique combination of arguments).

    Args:
        n_tickers: Number of synthetic tickers to generate. Defaults to 500.
        freq: Data frequency passed to :func:`sample_prices`. Defaults to ``"daily"``.
        max_bars: If greater than 0, return only the most recent ``max_bars`` rows
            per ticker. Defaults to 0 (all rows).

    Returns:
        Polars DataFrame with a leading ``ticker`` column followed by the same
        temporal and OHLCV columns as :func:`sample_prices`.
    """
    import polars as pl

    prices = sample_prices(freq=freq, backend="polars")
    if max_bars > 0:
        prices = prices.tail(max_bars)
    date_col = prices.columns[0]
    tickers = SAMPLE_TICKERS[:n_tickers]
    frames = [prices.with_columns(pl.lit(t).alias("ticker")) for t in tickers]
    return pl.concat(frames).sort("ticker", date_col)


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
