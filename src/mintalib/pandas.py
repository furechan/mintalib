import inspect
import warnings

import numpy as np
import pandas as pd

NAMESPACE = "ts"


def wrap_pandas(result, source, name: str = None):
    """ wrap result to pandas """

    if isinstance(result, tuple) and hasattr(result, '_asdict'):
        result = result._asdict()

    index = getattr(source, 'index', None)

    if isinstance(result, dict):
        return pd.DataFrame(result, index=index)

    if isinstance(result, np.ndarray):
        return pd.Series(result, index=index, name=name)

    return result



def wrap_method(func):
    sig = inspect.signature(func)
    fparam = list(sig.parameters.values())[0]

    def wrapper(self, *args, **kwargs):
        data = self._data
        if isinstance(data, pd.DataFrame) and fparam.name == "series":
            data = data['close']
        result = func(data, *args, **kwargs)
        return wrap_pandas(result, data)

    return wrapper



@pd.api.extensions.register_dataframe_accessor(NAMESPACE)
class DataFrameCalc:
    """DataFrame 'calc' accessor"""

    def __init__(self, data):
        self._data = data


@pd.api.extensions.register_series_accessor(NAMESPACE)
class SeriesCalc:
    """Series 'calc' accessor"""

    def __init__(self, data):
        self._data = data



def setup():
    from . import core

    calc_methods = [m for m in dir(core) if m.startswith("calc_")]

    for cname in calc_methods:
        name = cname.removeprefix("calc_")
        func = getattr(core, cname) 
        sig = inspect.signature(func)
        fparam = list(sig.parameters.values())[0]

        wrapper = wrap_method(func)
        setattr(DataFrameCalc, name, wrapper)

        if fparam.name == "series":
            wrapper = wrap_method(func)
            setattr(SeriesCalc, name, wrapper)

setup()


