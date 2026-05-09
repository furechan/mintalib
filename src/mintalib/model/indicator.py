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

    @abstractmethod
    def __call__(self, data): ...

    def __matmul__(self, other):
        import warnings
        if callable(other):
            warnings.warn(
                "indicator @ indicator is deprecated, use | instead",
                DeprecationWarning,
                stacklevel=2,
            )
            return ComposedIndicator(self, other)

        warnings.warn(
            "indicator @ data is deprecated, use data | indicator instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self(other)

    __pandas_priority__ = 5000

    def __or__(self, other):
        if isinstance(other, Indicator):
            return IndicatorChain(self, other)
        return NotImplemented

    def __ror__(self, other):
        if isinstance(other, Indicator):
            return IndicatorChain(other, self)
        return self(other)

    def get_series(self, data):
        """Series data accessor"""
        item = getattr(self, "item", None)
        return _get_series(data, item)

    def alias(self, name: str):
        return AliasedIndicator(self, name)


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


class ComposedIndicator(Indicator):
    """Composition of Indicators"""

    def __init__(self, *chain):
        items = []
        for item in chain:
            if isinstance(item, ComposedIndicator):
                items.extend(item.chain)
            else:
                items.append(item)
        self.chain = tuple(items)

    def __repr__(self):
        return " @ ".join(repr(fn) for fn in self.chain)

    def __call__(self, data):
        for fn in reversed(self.chain):
            data = fn(data)
        return data


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

    def __repr__(self):
        return " | ".join(repr(fn) for fn in self.chain)

    def __call__(self, data):
        for fn in self.chain:
            data = fn(data)
        return data

    def __ror__(self, other):
        if isinstance(other, Indicator):
            return IndicatorChain(other, *self.chain)
        return self(other)


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

