"""Generate src/mintalib/expressions.py"""

import inspect
from pathlib import Path
from pprint import pformat

from mintalib import core
from mintalib.builder import annotate_parameter

PACKAGE = "mintalib"
ROOTDIR = Path(__file__).parent.parent
PKGDIR = ROOTDIR.joinpath(f"src/{PACKAGE}").resolve(strict=True)

PRELUDE = '''# ty: ignore[empty-body] (decorator-replaces-body pattern: empty stubs are intentional)
"""
Polars Expression Factory Methods

Functions in this module are polars expression factories, typically named after
the indicator in upper case as in `SMA`, `EMA`, `MACD`.

This module is polars-only: factories build native polars expressions for use in
`select` or `with_columns` contexts. For pandas, use `mintalib.indicators` or `mintalib.functions`.

The optional `src` keyword parameter allows overriding the default input column.
For series-based indicators the default is the `close` column.
Price-based indicators use semantic keyword sources such as `high=`, `low=`,
`close=`, and `volume=`, defaulting to columns with those names.

Multi-output indicators like `MACD` and `BBANDS` return a polars struct expression
that can be unpacked with `.unnest()`.
"""

# Do not edit! This file was generated.

import polars as pl

from mintalib import core
from mintalib.model.expression import (
    CLOSE as CLOSE,
    ExprBundle as ExprBundle,
    OHLC as OHLC,
    IntoExpr,
)


'''


class Symbol(str):
    def __repr__(self):
        return self


def wrapper_name(calc_func):
    first_param = next(iter(inspect.signature(calc_func).parameters))
    if first_param == "series":
        return "wrap_series_expression"
    return "wrap_columns_expression"


def make_signature(calc_func):
    sig = inspect.signature(calc_func)
    params = list(sig.parameters.values())
    declared_inputs = getattr(calc_func, "metadata", {}).get("inputs")

    if params[0].name == "series":
        inputs: tuple[str, ...] = ()
    elif not declared_inputs:
        raise ValueError(f"Missing inputs metadata for {calc_func.__name__!r}")
    else:
        inputs = tuple(declared_inputs)

    new_params = []
    for param in params:
        if param.name == "series" or param.name in inputs:
            continue
        param = annotate_parameter(param)
        new_params.append(param)

    if params[0].name == "series":
        new_params.append(
            inspect.Parameter(
                name="src",
                default="close",
                kind=inspect.Parameter.KEYWORD_ONLY,
                annotation=Symbol("IntoExpr"),
            )
        )
    else:
        for name in inputs:
            new_params.append(
                inspect.Parameter(
                    name=name,
                    default=name,
                    kind=inspect.Parameter.KEYWORD_ONLY,
                    annotation=Symbol("IntoExpr"),
                )
            )

    return sig.replace(parameters=new_params, return_annotation=Symbol("pl.Expr"))


def make_expression(calc_func):
    cname = f"core.{calc_func.__name__}"
    fname = calc_func.__name__.removeprefix("calc_").upper()
    signature = make_signature(calc_func)
    decorator = wrapper_name(calc_func)
    buffer = f"@{decorator}({cname})\n"
    buffer += f"def {fname}{signature}: ...\n"
    return buffer


def core_functions():
    return sorted(k for k, v in vars(core).items() if k.startswith("calc_") and callable(v))


def make_expressions(cnames=None):
    if cnames is None:
        cnames = core_functions()

    funcs = [getattr(core, cname) for cname in cnames]
    wrappers = sorted({wrapper_name(func) for func in funcs})
    imports = "from mintalib.model.expression import (\n"
    imports += "".join(f"    {wrapper},\n" for wrapper in wrappers)
    imports += ")\n\n"
    output = PRELUDE + imports

    for cname, func in zip(cnames, funcs):
        code = make_expression(func)
        output += code + "\n"

    names = sorted(["ExprBundle", *(func.__name__.removeprefix("calc_").upper() for func in funcs)])
    exports = pformat(names, width=75, compact=True, indent=4)
    exports = exports.replace("[", " ").replace("]", "")
    output += f"__all__ = [\n{exports}\n]\n"

    return output


if __name__ == "__main__":
    output = make_expressions()
    outfile = PKGDIR / "expressions.py"
    print(f"Updating {outfile.name} ...")
    outfile.write_text(output)
