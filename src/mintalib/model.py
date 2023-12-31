""" Model classes """

from typing import ClassVar

from abc import ABC, abstractmethod

from inspect import Signature, Parameter


class LazyRepr:
    """Implements a basic __repr__ based on __init__ signature"""

    def __repr__(self):
        data = self.__dict__
        cname = self.__class__.__qualname__

        signature = Signature.from_callable(self.__init__)
        parameters = signature.parameters.values()
        positional = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)

        args, kwargs = [], {}

        for p in parameters:
            v = data.get(p.name, p.default)

            if p.kind in positional:
                args.append(v)

            elif v != p.default:
                kwargs[p.name] = v

        params = tuple(repr(p) for p in args) + tuple(
            "%s=%r" % kv for kv in kwargs.items()
        )
        params = ", ".join(params)

        return "%s(%s)" % (cname, params)


class Indicator(ABC, LazyRepr):
    """Abstact Base class for Indicators"""

    same_scale: ClassVar[bool] = False

    @abstractmethod
    def __call__(self, data):
        ...

    def __matmul__(self, other):
        if not callable(other):
            return self(other)
        return CallableChain(self, other)


class CallableChain:
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
