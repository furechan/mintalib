"""Indicator Model"""

import inspect

from typing import Callable
from types import MappingProxyType
from functools import cached_property

from abc import ABCMeta, abstractmethod
from typing import Protocol, Sequence, Any

from ..core import get_series, wrap_result, column_accessor
from ..utils import format_partial, lazy_repr


class DataFrameLike(Protocol):
    """Basic DataFrame Protocol for typing"""
    @property
    def columns(self) -> Sequence[Any]: ...
    def __getitem__(self, key: Any) -> Any: ...


class SeriesLike(Protocol):
    """Basic Series Protocol for typing"""
    @property
    def name(self) -> str | None: ...
    def to_numpy(self) -> Any: ...


class Indicator(metaclass=ABCMeta):
    """Abstact Base Class for Indicators"""

    __repr__ = lazy_repr

    @abstractmethod
    def __call__(self, data): ...

    def __matmul__(self, other):
        if callable(other):
            return ComposedIndicator(self, other)

        return self(other)

    def get_series(self, data):
        """Series data accessor"""
        item = getattr(self, "item", None)
        return get_series(data, item=item)

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

    output_name: str = None

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

    def __call__(self, prices):
        output_name = getattr(self, "output_name", None)

        if self.input_type == "series":
            series = get_series(prices, self.item)
            result = self.func(series, **self.params)
        else:
            prices = column_accessor(prices)
            result = self.func(prices, **self.params)

        return wrap_result(result, prices, name=output_name)


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
        wrapper.__doc__ = calc_func.__doc__
        wrapper.__signature__ = sig

        return wrapper

    return decorator

