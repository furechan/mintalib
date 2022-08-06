""" Indicator Base classes """

import pandas as pd

import inspect

from abc import ABC, abstractmethod

from .utils import export

import warnings


# TODO move indicator to a module named like model ??

# TODO remove clone from Indicator ?
# TODO create a make_indicator that wraps a function into an indicator ?
# TODO distinguish indicators that need a series from those that need a prices dataframe ?

# TODO Make a DataFrame abc instead of import pandas here ?


class ReprMixin:
    """ Mixin to implement a minimalist __repr__ based on __init__ signature """

    def __repr__(self):
        data = self.__dict__
        cname = self.__class__.__name__

        signature = inspect.signature(self.__init__)
        parameters = signature.parameters.values()
        positional = (inspect.Parameter.POSITIONAL_ONLY,
                      inspect.Parameter.POSITIONAL_OR_KEYWORD)

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

    def __or__(self, other):
        if not callable(other):
            return NotImplemented

        if hasattr(other, '__ror__'):
            return NotImplemented

        return IndicatorChain(self, other)

    def __matmul__(self, other):
        if not callable(other):
            return NotImplemented

        if hasattr(other, '__rmatmul__'):
            return NotImplemented

        return IndicatorComposition(self, other)

    def get_series(self, data):
        if callable(self.item):
            warnings.warn("callable item is legacy! use pipe operator instead.")
            return self.item(data)

        if isinstance(data, pd.DataFrame):
            if self.item is not None:
                return data[self.item]

            if self.default_item in data:
                return data[self.default_item]

            return data.iloc[:, 0]

        elif self.item:
            raise ValueError("Cannot specify item=f{self.item!r} with a series input!")

        return data

    def calc_cached(self, data):
        """ calc with builtin caching """

        key = self.__class__, *((k, self.__dict__[k]) for k in sorted(self.__dict__))
        cache = data.__dict__.setdefault('__cache__', {})

        try:
            return cache[key]
        except KeyError:
            result = self.calc(data)
            cache[key] = result
            return result

    def clone(self, **kwargs):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__, **kwargs)
        return result


@export
class IndicatorChain(Indicator):
    """ Chain of Indicators """

    def __init__(self, *indicators):
        self.indicators = indicators

    def __repr__(self):
        return " | ".join(repr(i) for i in self.indicators)

    def __or__(self, other):
        if not callable(other):
            return NotImplemented

        if hasattr(other, '__ror__'):
            return NotImplemented

        indicators = *self.indicators, other
        return self.__class__(*indicators)

    @property
    def main_indicator(self):
        if self.indicators:
            return self.indicators[-1]

    def calc(self, data):
        for indicator in self.indicators:
            data = indicator(data)
        return data


@export
class IndicatorComposition(Indicator):
    """ Composition of Indicators """

    def __init__(self, *indicators):
        self.indicators = indicators

    def __repr__(self):
        return " @ ".join(repr(i) for i in self.indicators)

    def __matmul__(self, other):
        if not callable(other):
            return NotImplemented

        if hasattr(other, '__rmatmul__'):
            return NotImplemented

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
