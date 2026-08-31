"""
Study interface intended to facilitate the composition of indicators.

A study combines multiple indicators applied to the same prices into a single
DataFrame result.

This module is pandas-only: studies accept and return pandas DataFrames.
For polars, use `mintalib.expressions` natively.
"""

from abc import ABCMeta, abstractmethod

from dataclasses import dataclass

import pandas as pd


class _StudyBase(metaclass=ABCMeta):
    """Shared calculation and merge behavior for studies."""

    __pandas_priority__ = 5000

    def calc(self, prices, *, merge: bool = False) -> pd.DataFrame:
        """Calculate the study columns, optionally merging them with the input."""
        if not isinstance(prices, pd.DataFrame):
            raise TypeError(
                f"{type(self).__name__} only accepts pandas DataFrames, got {type(prices).__name__}. "
                "For polars, use mintalib.expressions."
            )
        result = self._compute(prices)
        if not merge:
            return result

        merged = prices.copy()
        merged[result.columns] = result
        return merged

    def __call__(self, prices, *, merge: bool = False) -> pd.DataFrame:
        return self.calc(prices, merge=merge)

    @abstractmethod
    def _compute(self, prices: pd.DataFrame) -> pd.DataFrame: ...


class Study(_StudyBase):
    """Applies multiple indicators to the same prices and collects the results as columns of one DataFrame.

    Keyword argument names become column names, as in `Study(sma=SMA(20), ema=EMA(50))`.
    Positional arguments must yield results that carry their own name (a named Series or a DataFrame).
    """

    args: tuple = ()
    kwargs: dict = {}

    def items(self):
        for arg in self.args:
            yield None, arg
        for kv in self.kwargs.items():
            yield kv

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


    def __repr__(self):
        cname = self.__class__.__name__
        params = ", ".join(f"{k}={v!r}" if k else repr(v) for k, v in self.items())
        return f"{cname}({params})"


    def _compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        columns = dict()

        for name, func in self.items():
            result = func(prices)

            if hasattr(result, 'columns'):
                columns.update(result)
            elif name is not None:
                columns[name] = result
            elif hasattr(result, 'name'):
                columns[result.name] = result
            else:
                raise ValueError(f"Unexpected result type {type(result)!r} in positional args!")

        return pd.DataFrame(columns, index=prices.index)


@dataclass(frozen=True)
class Trail(_StudyBase):
    """Trailing values of a column: one column per lag, named `item0`, `item1`, ... for `skip <= n < windows`."""

    item: str
    windows: int
    skip: int = 0


    def _compute(self, prices: pd.DataFrame) -> pd.DataFrame:
        columns = {}
        series = prices[self.item]
        for n in range(self.skip, self.windows):
            name = f"{self.item}{n}"
            columns[name] = series.shift(n)

        return pd.DataFrame(columns, index=prices.index)


__all__ = ["Study", "Trail"]
