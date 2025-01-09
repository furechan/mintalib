"""Model classes"""

import sys
import inspect


from abc import ABCMeta, abstractmethod
from types import MappingProxyType
from functools import cached_property

from .utils import format_partial, lazy_repr
from .core import get_series, wrap_result

class StructWrapper:
    """Indicator wrapper to unnest/nest struct data"""
    def __init__(self, indicator):
        self.indicator = indicator
    
    def __getattr__(self, name):
        return getattr(self.indicator, name)
    
    def __repr__(self):
        return repr(self.indicator)
    
    def __call__(self, data):
        # Unnest data if applicable
        if hasattr(data, 'dtype') and data.dtype.__class__.__name__ == 'Struct':
            data = data.struct
        # Call indicator
        result = self.indicator(data)
        # Convert result to struct if applicable
        if hasattr(result, 'to_struct'):
            cname = self.indicator.__class__.__name__
            result = result.to_struct(cname.lower())
        return result


class Indicator(metaclass=ABCMeta):
    """Abstact Base class for Indicators"""

    same_scale: bool = False

    __repr__ = lazy_repr

    @abstractmethod
    def __call__(self, data): ...

    @property
    @abstractmethod
    def input_type(self):
        """input type: wether "series" or "prices"""
        ...

    def __matmul__(self, other):
        if hasattr(other, 'map_batches'): # polars expression
            polars = sys.modules.get("polars")
            if str(other) == "*" and polars:
                other = polars.struct(other)
            elif self.input_type != "series":
                raise NotImplementedError
            wrapper = StructWrapper(self)
            return other.map_batches(wrapper)

        if callable(other):
            return CallableChain(self, other)
        
        return self(other)
        

 

class FuncIndicator(Indicator):
    """Function based Indicator"""

    def __init__(self, func, params: dict):
        self.func = func
        self.item = params.pop('item', None)
        self.params = MappingProxyType(params)

    @cached_property
    def input_type(self):
        signature = inspect.signature(self.func)
        return next(iter(signature.parameters), None) 

    def __getattr__(self, name):
        return getattr(self.func, name)

    def __repr__(self):
        return format_partial(self.func, self.kwargs)

    def __call__(self, prices):
        if self.input_type == "series":
            series = get_series(prices, self.item)
            result = self.func(series, **self.params)
        else:
            result = self.func(prices, **self.params)

        return wrap_result(result, prices)  

    
class FuncWrapper(Indicator):
    """Function based Indicator"""

    def __init__(self, func, params: dict):
        self.func = func
        self.item = params.pop('item', None)
        self.params = MappingProxyType(params)

    @cached_property
    def input_type(self):
        signature = inspect.signature(self.func)
        return next(iter(signature.parameters), None) 

    def __getattr__(self, name):
        return getattr(self.func, name)

    def __repr__(self):
        return format_partial(self.func, self.kwargs)

    def __call__(self, prices):
        if self.input_type == "series":
            series = get_series(prices, self.item)
            result = self.func(series, **self.params)
        else:
            result = self.func(prices, **self.params)

        return wrap_result(result, prices)  

    


class CallableChain(Indicator):
    """Chain of Callables"""

    def __init__(self, *chain):
        items = []
        for item in chain:
            if isinstance(item, CallableChain):
                items.extend(item.chain)
            else:
                items.append(item)
        self.chain = tuple(items)

    @cached_property
    def input_type(self):
        if self.chain:
            return self.chain[-1].input_type

    def __repr__(self):
        return " @ ".join(repr(fn) for fn in self.chain)

    def __call__(self, data):
        for fn in reversed(self.chain):
            data = fn(data)
        return data

