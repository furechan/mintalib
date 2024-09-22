"""Model classes"""


from abc import ABC, abstractmethod

from inspect import Signature, Parameter


def lazy_repr(obj):
    data = obj.__dict__
    cname = obj.__class__.__qualname__

    signature = Signature.from_callable(obj.__init__)
    parameters = signature.parameters.values()
    positional = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)

    arguments = []

    for p in parameters:
        v = data.get(p.name, p.default)
        if p.kind in positional:
            arguments.append(f"{v!r}")
        elif v != p.default:
            arguments.append(f"{p.name}={v!r}")

    arguments = ", ".join(arguments)

    return "%s(%s)" % (cname, arguments)


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
