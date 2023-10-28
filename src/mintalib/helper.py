""" helper utilities """


from typing import Callable

from inspect import Signature, Parameter


def func_type(func: Callable) -> str:
    """Function type according to its first parameter (series or prices)"""

    signature = Signature.from_callable(func)
    params = list(signature.parameters.values())

    if params and params[0].name in ('series', 'prices'):
        return params[0].name

    return 'other'


def sample_param(param: Parameter):
    """Sample value for parameters without ac default value"""

    if param.name == 'expr':
        return 'close'
    if param.name == 'period':
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
        if param.name in ('series', 'prices'):
            continue
        value = sample_param(param)
        kwds[param.name] = value

    return kwds

