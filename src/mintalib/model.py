""" Indicator Base classes """

from inspect import Signature, Parameter

from abc import ABC, abstractmethod


def export(func):
    globals().setdefault('__all__', []).append(func.__name__)
    return func


class ReprMixin:
    """ Mixin to implement a basic __repr__ based on __init__ signature """

    def __repr__(self):
        data = self.__dict__
        cname = self.__class__.__qualname__

        signature = Signature.from_callable(self.__init__)
        parameters = signature.parameters.values()
        positional = (Parameter.POSITIONAL_ONLY,
                      Parameter.POSITIONAL_OR_KEYWORD)

        args, kwargs = [], {}

        for p in parameters:
            v = data.get(p.name, p.default)

            if p.kind in positional:
                args.append(v)

            elif v != p.default:
                kwargs[p.name] = v

        params = tuple(repr(p) for p in args) + tuple("%s=%r" % kv for kv in kwargs.items())
        params = ", ".join(params)

        return "%s(%s)" % (cname, params)


@export
class Indicator(ABC, ReprMixin):
    """ Abstact Base class for Indicators """

    default_item = 'close'
    same_scale = False
    item = None

    @abstractmethod
    def calc(self, data):
        ...

    def __call__(self, data):
        return self.calc(data)

    def __matmul__(self, other):
        if not callable(other):
            return self.calc(other)

        return IndicatorComposition(self, other)

    def get_series(self, data):
        if hasattr(data, 'columns'):
            item = self.item or self.default_item
            return data[item]

        elif self.item:
            raise ValueError("Cannot specify item=f{self.item!r} with a series input!")

        return data

    def clone(self, **kwargs):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__, **kwargs)
        return result


@export
class IndicatorComposition(Indicator):
    """ Composition of Indicators """

    def __init__(self, *indicators):
        self.indicators = indicators

    def __repr__(self):
        return " @ ".join(repr(i) for i in self.indicators)

    def __matmul__(self, other):
        if not callable(other):
            return self.calc(other)

        indicators = *self.indicators, other
        return self.__class__(*indicators)

    @property
    def main_indicator(self):
        if self.indicators:
            return self.indicators[0]

    def calc(self, data):
        for indicator in reversed(self.indicators):
            data = indicator(data)
        return data
