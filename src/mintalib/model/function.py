"""Function Model"""

import inspect

from ..core import get_series, wrap_result, column_accessor


def wrap_function(calc_func):
    """Decorator to wrap indicators"""

    sig = inspect.signature(calc_func)
    first_param = next(iter(sig.parameters))

    def decorator(func):
        sig = inspect.signature(func)

        def wrapper(prices, *args, **kwargs):
            item = kwargs.pop('item', None)

            if first_param == 'series':
                input = get_series(prices, item)
            else:
                input = column_accessor(prices)

            result = calc_func(input, *args, **kwargs)
            return wrap_result(result, prices)

        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__doc__ = calc_func.__doc__
        wrapper.__signature__ = sig

        return wrapper
    return decorator

