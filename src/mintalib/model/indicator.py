"""Indicator Model"""

import inspect

import numpy as np
import pandas as pd

from typing import Callable
from types import MappingProxyType
from functools import cached_property
from abc import ABCMeta, abstractmethod

from ..utils import format_partial, lazy_repr


def _get_series(data, item: str | None = None):
    if isinstance(data, pd.DataFrame):
        return data[item or "close"]
    return data


def _wrap_result(result, source, name: str | None = None):
    if isinstance(result, tuple) and hasattr(result, "_asdict"):
        result = result._asdict()

    index = source.index if isinstance(source, (pd.DataFrame, pd.Series)) else None

    if isinstance(result, dict):
        return pd.DataFrame(result, index=index)

    if isinstance(result, np.ndarray):
        return pd.Series(result, index=index, name=name)

    return result


class Indicator(metaclass=ABCMeta):
    """Abstact Base Class for Indicators"""

    __repr__ = lazy_repr

    output_names: tuple[str, ...] | None = None

    __pandas_priority__ = 5000

    @abstractmethod
    def __call__(self, data): ...

    def __or__(self, other):
        if isinstance(other, Indicator):
            return IndicatorChain(self, other)
        raise TypeError(
            f"| chains indicators only; "
            f"to apply {self!r} to data, use data | {self!r}."
        )

    def __ror__(self, other):
        if isinstance(other, (pd.DataFrame, pd.Series)):
            return self(other)
        raise TypeError(
            f"| applies an indicator to a pandas DataFrame or Series; "
            f"got {type(other).__name__} on the left."
        )

    def get_series(self, data):
        """Series data accessor"""
        item = getattr(self, "item", None)
        return _get_series(data, item)

    def alias(self, name: str):
        return AliasedIndicator(self, name)

    def then(self, other):
        """Chain another indicator after this one (fluent equivalent of `|`)."""
        if not isinstance(other, Indicator):
            raise TypeError(
                f".then() chains indicators; got {type(other).__name__}."
            )
        return IndicatorChain(self, other)

    def as_expr(self):
        if self.output_names:
            names = ", ".join(self.output_names)
            raise TypeError(
                f"as_expr() requires a single-output indicator; "
                f"{self!r} produces multiple outputs ({names})."
            )
        try:
            from pandas.api.typing import Expression
        except ImportError as exc:
            raise RuntimeError(
                f"as_expr() requires pandas >= 3.0 (got {pd.__version__}); "
                "the Expression API was introduced in pandas 3.0."
            ) from exc
        return Expression(self, repr(self))


class AliasedIndicator(Indicator):
    """Aliased Indicator"""

    def __init__(self, indicator, name):
        self.indicator = indicator
        self.name = name
    
    def __repr__(self):
        return f"{self.indicator!r}.alias({self.name!r})"

    def __call__(self, data):
        result = self.indicator(data)
        rtype = type(result).__name__

        if rtype == "Series" and hasattr(result, "rename"):
            return result.rename(self.name)

        raise ValueError(f"Cannot rename {rtype} result")



class FuncIndicator(Indicator):
    """Function Based Indicator"""

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

    @cached_property
    def output_names(self):
        metadata = getattr(self, "metadata", None)
        names = metadata.get("output_names") if metadata else None
        return tuple(names) if names else None

    def __repr__(self):
        return format_partial(self.func, self.params, name=self.name)

    def __call__(self, data):
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



class IndicatorChain(Indicator):
    """Chain of Indicators applied left-to-right (created by the | operator)"""

    def __init__(self, *chain):
        items = []
        for item in chain:
            if isinstance(item, IndicatorChain):
                items.extend(item.chain)
            else:
                items.append(item)
        self.chain = tuple(items)

    @property
    def output_names(self):
        return self.chain[-1].output_names if self.chain else None

    def __repr__(self):
        return " | ".join(repr(fn) for fn in self.chain)

    def __call__(self, data):
        for fn in self.chain:
            data = fn(data)
        return data


def wrap_indicator(calc_func):
    """Decorator to wrap indicators"""

    def decorator(func):
        name = func.__name__
        sig = inspect.signature(func)

        def wrapper(*args, **kwargs):
            binding = sig.bind(*args, **kwargs)
            binding.apply_defaults()
            params = dict(binding.arguments)

            return FuncIndicator(
                name=name,
                func=calc_func,
                params=params,
            )

        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__module__ = func.__module__
        wrapper.__doc__ = calc_func.__doc__
        wrapper.__signature__ = sig  # ty: ignore[unresolved-attribute]

        return wrapper

    return decorator


class EVAL(Indicator):
    """Evaluate a pandas expression against a DataFrame's columns."""

    def __init__(self, expr: str, *, as_flag: bool = False):
        self.expr = expr
        self.as_flag = as_flag

    def __repr__(self):
        if self.as_flag:
            return f"EVAL({self.expr!r}, as_flag=True)"
        return f"EVAL({self.expr!r})"

    def __call__(self, data):
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

