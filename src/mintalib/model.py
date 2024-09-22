"""Model classes"""

from abc import ABC, abstractmethod

from .utils import format_partial, lazy_repr


class Indicator(ABC):
    """Abstact Base class for Indicators"""

    same_scale: bool = False

    __repr__ = lazy_repr

    @abstractmethod
    def __call__(self, data): ...

    def __matmul__(self, other):
        if not callable(other):
            return self(other)
        return CallableChain(self, other)


class FuncIndicator(Indicator):
    def __init__(self, func, params: dict, name: str):
        self.func = func
        self.params = params
        self.name = name

    def __repr__(self):
        return self.name

    def __call__(self, prices):
        return self.func(prices, **self.params)

    @classmethod
    def wrap(cls, func, params: dict):
        name = format_partial(func, params)
        return cls(func, params=params, name=name)


class CallableChain(Indicator):
    """Chain of Callables"""

    def __init__(self, *chain):
        self.chain = chain

    def __repr__(self):
        return " @ ".join(repr(fn) for fn in self.chain)

    def __call__(self, data):
        for fn in reversed(self.chain):
            data = fn(data)
        return data

    def __matmul__(self, other):
        if not callable(other):
            return self(other)
        return self.__class__(*self.chain, other)
