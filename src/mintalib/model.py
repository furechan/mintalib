"""Model classes"""

from abc import ABCMeta, abstractmethod
from types import MappingProxyType

from .utils import format_partial, lazy_repr


class Indicator(metaclass=ABCMeta):
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
    """Function based Indicator"""
    def __init__(self, func, params: dict):
        self.func = func
        self.params = MappingProxyType(params)

    def __getattr__(self, name):
        return getattr(self.func, name)

    def __repr__(self):
        return format_partial(self.func, self.params)

    def __call__(self, prices):
        return self.func(prices, **self.params)
    

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
