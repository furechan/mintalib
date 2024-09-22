"""Mintalib Utils"""

from inspect import Signature, Parameter


def format_partial(func, params):
    signature = Signature.from_callable(func)
    positional = True
    arguments = []

    for k, v in params.items():
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
    return "%s(%s)" % (func.__name__, arguments)


def lazy_repr(obj):
    data = obj.__dict__
    cname = obj.__class__.__qualname__

    signature = Signature.from_callable(obj.__init__)
    parameters = signature.parameters.values()
    positional = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)

    arguments = []

    for p in parameters:
        v = data.get(p.name, p.default)
        if p.kind in positional:
            arguments.append(f"{v!r}")
        elif v != p.default:
            arguments.append(f"{p.name}={v!r}")

    arguments = ", ".join(arguments)

    return "%s(%s)" % (cname, arguments)
