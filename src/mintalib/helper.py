""" testing utilities """

import numpy as np

from typing import Callable

from inspect import Signature, Parameter


def func_type(func: Callable) -> str:
    signature = Signature.from_callable(func)
    params = list(signature.parameters.values())

    if params and params[0].name in ('series', 'prices'):
        return params[0].name

    return 'other'


def sample_param(param: Parameter):
    if param.name == 'expr':
        return 'close'
    if param.name == 'period':
        return 20
    raise NameError(param.name)


def sample_params(func: Callable) -> dict:
    kwds = dict()

    signature = Signature.from_callable(func)
    parameters = list(signature.parameters.values())

    for param in parameters:
        if param.default != param.empty:
            continue
        if param.name in ('series', 'prices'):
            continue
        value = sample_param(param)
        kwds[param.name] = value

    return kwds


def compare_results(result, target):
    return np.allclose(result, target, equal_nan=True)
