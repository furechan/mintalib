""" helper utilities """


from typing import Callable

from inspect import Signature, Parameter


def first_param(func: Callable):
    """Name of function's first parameter if any"""
    params = Signature.from_callable(func).parameters
    return next(params.__iter__(), None)


def sample_param(param: Parameter):
    """Sample value for parameters without ac default value"""

    if param.name == "expr":
        return "close"
    if param.name == "period":
        return 20
    raise NameError(param.name)


def sample_params(func: Callable) -> dict:
    """Dictionary of sample parameter values"""

    kwds = dict()

    signature = Signature.from_callable(func)
    parameters = list(signature.parameters.values())

    for param in parameters:
        if param.default != param.empty:
            continue
        if param.name in ("series", "prices"):
            continue
        value = sample_param(param)
        kwds[param.name] = value

    return kwds
