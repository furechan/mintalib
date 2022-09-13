""" helper routines """

import inspect
import collections

import pandas as pd


def get_info(func):
    """ information acount function/indicator """
    info = dict(name=func.__qualname__)
    params = list(inspect.signature(func).parameters.values())
    if params and params[0].name in ('series', 'prices'):
        info.update(input=params[0].name)
    doc = func.__doc__ or ""
    description = doc.strip().partition("\n")[0]
    if description is not None:
        info.update(description=description)
    return info


def list_functions():
    """ list functions """

    from . import functions

    result = []
    for k, v in vars(functions).items():
        if callable(v) and v.__name__.isupper():
            result.append(v)

    result = [get_info(f) for f in result]

    result = pd.DataFrame(result).set_index('name')

    return result


def list_indicators():
    """ list indicators from core """

    from . import indicators

    def check_indicator(obj):
        return isinstance(obj, type) and obj.__name__.isupper()

    result = []
    queue = collections.deque([indicators])

    while queue:
        item = queue.popleft()
        for k, v in vars(item).items():
            if check_indicator(v):
                queue.append(v)
                result.append(v)

    result = [get_info(f) for f in result]

    result = pd.DataFrame(result).set_index('name')

    return result
