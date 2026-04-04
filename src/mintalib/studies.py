"""mintalib studies"""

import functools

from abc import ABCMeta, abstractmethod

from dataclasses import dataclass

from .utils import detect_backend


class Study(metaclass=ABCMeta):
    """callable/chainable with process method and composition"""

    __pandas_priority__ = 5000

    @abstractmethod
    def __call__(self, prices): ...

    def __or__(self, other):
        """pipe into callable"""

        if not callable(other):
            return NotImplemented

        return self.pipe(other)


    def pipe(self, func, **kwargs):
        """pipe into callable with optional arguments"""

        if kwargs:
            func = functools.partial(func, **kwargs)

        return ChainedStudy(self, func)


class ChainedStudy(Study):
    """chain of callables/studies"""

    funcs: tuple = ()

    def __init__(self, *funcs):
        for func in funcs:
            if not callable(func):
                raise TypeError(f"Argument {func!r} is not callable!")
        self.funcs = funcs

    def __repr__(self):
        return " | ".join(repr(fn) for fn in self.funcs)

    def __call__(self, prices):
        result = prices
        
        for func in self.funcs:
            if result is None:
                return
            result = func(result)

        return result

    def pipe(self, func, **kwargs):
        """pipe into callable with optional arguments"""

        if kwargs:
            func = functools.partial(func, **kwargs)

        funcs = self.funcs + (func,)
        return self.__class__(*funcs)




class QuickStudy(Study):
    """Update Study"""

    args: tuple = ()
    kwargs: dict = {}

    def items(self):
        for arg in self.args:
            yield None, arg
        for kv in self.kwargs.items():
            yield kv
        
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


    def __repr__(self):
        cname = self.__class__.__name__
        params = ", ".join(f"{k}={v!r}" if k else repr(v) for k, v in self.items())
        return f"{cname}({params})"


    def __call__(self, prices):
        if not hasattr(prices, 'columns'):
            raise ValueError("DataFrame expected!")

        backend = detect_backend(prices)

        if backend == "pandas":
            return self.apply_pandas(prices)
        
        if backend == "polars":
            return self.apply_polars(prices)
        
        raise ValueError(f"Unsupported DataFrame type: {backend}")
       
    
    def apply_pandas(self, prices):
        import pandas as pd

        columns = dict()
        
        for name, func in self.items():
            result = func(prices)

            if hasattr(result, 'columns'):
                columns.update(result)
            elif name is not None:
                columns[name] = result
            elif hasattr(result, 'name'):
                columns[result.name] = result
            else:
                raise ValueError(f"Unexpected result type {type(result)!r} in positional args!")
                
        return pd.DataFrame(columns, index=prices.index)


    def apply_polars(self, prices):
        import polars as pl

        columns = dict()

        for name, func in self.items():
            result = func(prices)

            if hasattr(result, 'columns'):
                columns.update(result.to_dict())
            elif name is not None:
                columns[name] = result
            elif hasattr(result, 'name'):
                columns[result.name] = result
            else:
                raise ValueError(f"Unexpected result type {type(result)!r} in positional args!")

        return pl.DataFrame(columns)


@dataclass(frozen=True)
class Trail(Study):
    """Trailing values"""

    item: str
    windows: int
    skip : int = 0


    def __call__(self, prices):
        if not hasattr(prices, 'columns'):
            raise ValueError("DataFrame expected!")

        backend = detect_backend(prices)

        if backend == "pandas":
            return self.apply_pandas(prices)
        
        if backend == "polars":
            return self.apply_polars(prices)
        
        raise ValueError(f"Unsupported DataFrame type: {backend}")
       
    def apply_pandas(self, data):
        import pandas as pd

        columns = {}
        series = data[self.item]
        for n in range(self.skip, self.windows):
            name = f"{self.item}{n}"
            columns[name] = series.shift(n)

        return pd.DataFrame(columns, index=data.index)

    def apply_polars(self, data):
        import polars as pl

        columns = {}
        series = data[self.item]
        for n in range(self.skip, self.windows):
            name = f"{self.item}{n}"
            columns[name] = series.shift(n)

        return pl.DataFrame(columns)
