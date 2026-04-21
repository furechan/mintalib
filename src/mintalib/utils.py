"""Mintalib Utils"""

from inspect import Signature, Parameter

def detect_backend(data) -> str:
    """Detect the backend of a data object ('pandas', 'polars', or '')."""
    return (getattr(data, '__module__', None) or '').partition('.')[0]


def get_metadata(func, name: str, default=None):
    """get metadata for a function"""
    return getattr(func, 'metadata', {}).get(name, default)


def format_partial(func, data, *, name: str | None = None):
    """format a partial function call"""

    if name is None:
        name = func.__name__

    signature = Signature.from_callable(func)
    positional = True
    arguments = []

    for k, v in data.items():
        p = signature.parameters.get(k)

        if not p or p.kind not in (
            Parameter.POSITIONAL_ONLY,
            Parameter.POSITIONAL_OR_KEYWORD,
        ):
            positional = False

        if positional:
            arguments.append(f"{v!r}")
        elif not p or v != p.default:
            arguments.append(f"{k!s}={v!r}")

    arguments = ", ".join(arguments)
    return "%s(%s)" % (name, arguments)


def lazy_repr(obj):
    """minimal __repr__ based on __init__ signature"""

    cname = obj.__class__.__qualname__

    return format_partial(obj.__init__, obj.__dict__, name=cname)

