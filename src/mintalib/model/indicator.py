"""Indicator Model"""

import inspect

import numpy as np
import pandas as pd

from typing import TYPE_CHECKING, Callable, ParamSpec, Any, cast, overload
from types import MappingProxyType
from functools import cached_property
from abc import ABCMeta, abstractmethod

from ..utils import format_partial, lazy_repr

if TYPE_CHECKING:
    from pandas.api.typing import Expression

P = ParamSpec("P")


def _get_series(data, item: str | None = None) -> pd.Series | np.ndarray:
    if isinstance(data, pd.DataFrame):
        return data[item or "close"]
    return data


def _wrap_result(result, source, name: str | None = None) -> pd.Series | pd.DataFrame:
    asdict = getattr(result, "_asdict", None)
    if isinstance(result, tuple) and asdict is not None:
        result = asdict()

    index = source.index if isinstance(source, (pd.DataFrame, pd.Series)) else None

    if isinstance(result, dict):
        return pd.DataFrame(result, index=index)

    if isinstance(result, np.ndarray):
        return pd.Series(result, index=index, name=name)

    raise TypeError(f"Unexpected result type {type(result).__name__}")


def _make_expression(func, repr_str: str) -> "Expression":
    try:
        from pandas.api.typing import Expression
    except ImportError as exc:
        raise RuntimeError(
            f"as_expr() requires pandas >= 3.0 (got {pd.__version__}); "
            "the Expression API was introduced in pandas 3.0."
        ) from exc

    return Expression(func, repr_str)  # pyright: ignore[reportCallIssue]


class Indicator(metaclass=ABCMeta):
    """Abstact Base Class for Indicators"""

    __repr__ = lazy_repr

    @abstractmethod
    def __call__(
        self, data: pd.DataFrame | pd.Series | np.ndarray
    ) -> pd.Series | pd.DataFrame: ...

    def _chain(self, other: "Indicator") -> "SeriesIndicator | FrameIndicator":
        if isinstance(other, SeriesIndicator):
            return SeriesIndicatorChain(self, other)
        if isinstance(other, FrameIndicator):
            return FrameIndicatorChain(self, other)
        raise TypeError(f"cannot chain {type(other).__name__}.")

    @overload
    def __or__(self, other: "SeriesIndicator") -> "SeriesIndicator": ...
    @overload
    def __or__(self, other: "FrameIndicator") -> "FrameIndicator": ...
    def __or__(self, other) -> "SeriesIndicator | FrameIndicator":
        if not isinstance(other, Indicator):
            raise TypeError(
                f"| chains indicators only; got {type(other).__name__}."
            )
        return self._chain(other)

    def get_series(self, data) -> pd.Series | np.ndarray:
        """Series data accessor"""
        item = getattr(self, "item", None)
        return _get_series(data, item)

    @overload
    def then(self, other: "SeriesIndicator") -> "SeriesIndicator": ...
    @overload
    def then(self, other: "FrameIndicator") -> "FrameIndicator": ...
    def then(self, other) -> "SeriesIndicator | FrameIndicator":
        """Chain another indicator after this one (fluent equivalent of `|`)."""
        if not isinstance(other, Indicator):
            raise TypeError(
                f".then() chains indicators; got {type(other).__name__}."
            )
        return self._chain(other)


class SeriesIndicator(Indicator):
    """Indicator with a single series output"""

    @abstractmethod
    def __call__(
        self, data: pd.DataFrame | pd.Series | np.ndarray
    ) -> pd.Series: ...

    def alias(self, name: str) -> "AliasedIndicator":
        return AliasedIndicator(self, name)

    def as_expr(self) -> "Expression":
        """Deferred pandas expression evaluating this indicator (pandas >= 3.0)."""
        return _make_expression(self, repr(self))


class FrameIndicator(Indicator):
    """Indicator with multiple outputs, returned as a DataFrame"""

    output_names: tuple[str, ...]

    @abstractmethod
    def __call__(
        self, data: pd.DataFrame | pd.Series | np.ndarray
    ) -> pd.DataFrame: ...

    def __getitem__(self, item: str) -> SeriesIndicator:
        if item not in self.output_names:
            names = ", ".join(self.output_names)
            raise KeyError(f"{item!r}: unknown output column. Valid: {names}.")
        return ItemIndicator(self, item)

    def as_expr(self, item: str) -> "Expression":
        """Deferred pandas expression for one output column (pandas >= 3.0)."""
        return self[item].as_expr()


class AliasedIndicator(SeriesIndicator):
    """Aliased Indicator"""

    def __init__(self, indicator: SeriesIndicator, name: str):
        self.indicator = indicator
        self.name = name

    def __repr__(self):
        return f"{self.indicator!r}.alias({self.name!r})"

    def __call__(self, data) -> pd.Series:
        return self.indicator(data).rename(self.name)


class ItemIndicator(SeriesIndicator):
    """Single output column of a multi-output indicator"""

    def __init__(self, indicator: FrameIndicator, item: str):
        self.indicator = indicator
        self.item = item

    def __repr__(self):
        return f"{self.indicator!r}[{self.item!r}]"

    def __call__(self, data) -> pd.Series:
        return self.indicator(data)[self.item]


class FuncIndicator(Indicator):
    """Function Based Indicator (common base for series/frame variants)"""

    output_name: str | None = None

    @staticmethod
    def indicator_name(func):
        name = func.__name__
        name = name.removeprefix("calc_")
        name = name.upper()
        return name

    def __init__(self, name: str, func: Callable, params: dict):
        self.name = name
        self.func = func
        self.item = params.pop("item", None)
        self.params = MappingProxyType(params)

        metadata = getattr(func, "metadata", None)
        if metadata:
            self.metadata = MappingProxyType(metadata)

    @cached_property
    def input_type(self):
        signature = inspect.signature(self.func)
        return next(iter(signature.parameters), None)

    def __repr__(self):
        return format_partial(self.func, self.params, name=self.name)

    def _compute(self, data) -> pd.Series | pd.DataFrame:
        if not isinstance(data, (pd.DataFrame, pd.Series, np.ndarray)):
            raise TypeError(
                f"{self.name} indicator only accepts pandas DataFrames, Series, or numpy arrays, "
                f"got {type(data).__name__}. For polars, use mintalib.expressions."
            )

        output_name = getattr(self, "output_name", None)

        if self.input_type == "series":
            series = _get_series(data, self.item)
            result = self.func(series, **self.params)
        else:
            if not isinstance(data, pd.DataFrame):
                raise TypeError(
                    f"{self.name} indicator requires a pandas DataFrame with OHLCV columns, "
                    f"got {type(data).__name__}."
                )
            result = self.func(data, **self.params)

        return _wrap_result(result, data, name=output_name)


class SeriesFuncIndicator(FuncIndicator, SeriesIndicator):
    """Function based indicator with a single series output"""

    def __call__(self, data) -> pd.Series:
        return cast(pd.Series, self._compute(data))


class FrameFuncIndicator(FuncIndicator, FrameIndicator):
    """Function based indicator with multiple outputs"""

    @cached_property
    def output_names(self) -> tuple[str, ...]:
        metadata = getattr(self, "metadata", None)
        names = metadata.get("output_names") if metadata else None
        if not names:
            raise TypeError(f"{self.name} is missing output_names metadata")
        return tuple(names)

    def __call__(self, data) -> pd.DataFrame:
        return cast(pd.DataFrame, self._compute(data))


class IndicatorChain(Indicator):
    """Chain of Indicators applied left-to-right (created by the | operator)"""

    chain: tuple[Indicator, ...]

    def __init__(self, *chain):
        items = []
        for item in chain:
            if isinstance(item, IndicatorChain):
                items.extend(item.chain)
            else:
                items.append(item)
        self.chain = tuple(items)

    def __repr__(self):
        return " | ".join(repr(fn) for fn in self.chain)

    def _run(self, data):
        for fn in self.chain:
            data = fn(data)
        return data


class SeriesIndicatorChain(IndicatorChain, SeriesIndicator):
    """Chain ending in a series indicator"""

    def __call__(self, data) -> pd.Series:
        return cast(pd.Series, self._run(data))


class FrameIndicatorChain(IndicatorChain, FrameIndicator):
    """Chain ending in a multi-output indicator"""

    @property
    def output_names(self) -> tuple[str, ...]:  # pyright: ignore[reportIncompatibleVariableOverride]
        return cast(FrameIndicator, self.chain[-1]).output_names

    def __call__(self, data) -> pd.DataFrame:
        return cast(pd.DataFrame, self._run(data))


def _wrap_func_indicator(calc_func, cls: type[FuncIndicator]):
    def decorator(func):
        name = func.__name__
        sig = inspect.signature(func)

        def wrapper(*args, **kwargs):
            binding = sig.bind(*args, **kwargs)
            binding.apply_defaults()
            params = dict(binding.arguments)

            return cls(name=name, func=calc_func, params=params)

        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__module__ = func.__module__
        wrapper.__doc__ = calc_func.__doc__
        wrapper.__signature__ = sig  # ty: ignore[unresolved-attribute]

        return wrapper

    return decorator


def wrap_series_indicator(
    calc_func,
) -> Callable[[Callable[P, Any]], Callable[P, SeriesIndicator]]:
    """Decorator to wrap single-output indicators"""
    return _wrap_func_indicator(calc_func, SeriesFuncIndicator)


def wrap_frame_indicator(
    calc_func,
) -> Callable[[Callable[P, Any]], Callable[P, FrameIndicator]]:
    """Decorator to wrap multi-output indicators"""
    return _wrap_func_indicator(calc_func, FrameFuncIndicator)


class EVAL(SeriesIndicator):
    """Evaluate a pandas expression against a DataFrame's columns."""

    def __init__(self, expr: str, *, as_flag: bool = False):
        self.expr = expr
        self.as_flag = as_flag

    def __repr__(self):
        if self.as_flag:
            return f"EVAL({self.expr!r}, as_flag=True)"
        return f"EVAL({self.expr!r})"

    def __call__(self, data) -> pd.Series:
        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                f"EVAL only accepts pandas DataFrames, got {type(data).__name__}. "
                "For polars, use mintalib.expressions."
            )

        result = np.asarray(data.eval(self.expr), dtype=float)

        if self.as_flag:
            from mintalib.core import calc_flag
            result = calc_flag(result)

        return pd.Series(result, index=data.index)
