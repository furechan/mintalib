"""Generate src/mintalib/expressions.py"""

import inspect
from pathlib import Path

PACKAGE = "mintalib"
ROOTDIR = Path(__file__).parent.parent
PKGDIR = ROOTDIR.joinpath(f"src/{PACKAGE}").resolve(strict=True)

from mintalib import core
from mintalib.builder import annotate_parameter
from mintalib.utils import get_metadata

PRELUDE = '''"""
Polars Expression Factory Methods

Functions in this module are polars expression factories, typically named after
the indicator in upper case as in `SMA`, `EMA`, `MACD`.

The optional `src` keyword parameter allows overriding the default input column.
For series-based indicators the default is `CLOSE` (i.e. `pl.col("close")`).
For price-based indicators `src` is not applicable and should be left as `None`.

Multi-output indicators like `MACD` and `BBANDS` return a polars struct expression
that can be unpacked with `.unnest()`.
"""

# Do not edit! This file was generated.

import polars as pl

from typing import TypeAlias

from mintalib import core
from mintalib.model.expression import wrap_expression

IntoExpr: TypeAlias = pl.Expr | str | None
"""Type alias for polars expressions accepted as inputs (pl.Expr, column name, or None)."""

CLOSE = pl.col(\'close\')
"""Expression for the close price column."""

OHLC = pl.struct([\'open\', \'high\', \'low\', \'close\'])
"""Expression for open, high, low, close columns as a struct."""


'''


class Symbol(str):
    def __repr__(self):
        return self


def make_signature(calc_func):
    sig = inspect.signature(calc_func)
    output_names = get_metadata(calc_func, "output_names")

    new_params = []
    for param in sig.parameters.values():
        if param.name in ("prices", "series"):
            continue
        param = annotate_parameter(param)
        new_params.append(param)

    src = inspect.Parameter(
        name="src",
        default=None,
        kind=inspect.Parameter.KEYWORD_ONLY,
        annotation=Symbol("IntoExpr | None"),
    )
    new_params.append(src)

    return_annotation = tuple if output_names else Symbol("pl.Expr")
    return sig.replace(parameters=new_params, return_annotation=return_annotation)


def make_expression(calc_func):
    cname = f"core.{calc_func.__name__}"
    fname = calc_func.__name__.removeprefix("calc_").upper()
    signature = make_signature(calc_func)
    buffer = f"@wrap_expression({cname})\n"
    buffer += f"def {fname}{signature}: ...\n"
    return buffer


def core_functions(exclude=("calc_eval",)):
    names = sorted(k for k, v in vars(core).items() if k.startswith("calc_") and callable(v))
    if exclude:
        names = [n for n in names if n not in exclude]
    return names


def make_expressions(cnames=None):
    if cnames is None:
        cnames = core_functions()

    output = PRELUDE

    for cname in cnames:
        func = getattr(core, cname)
        code = make_expression(func)
        output += code + "\n"

    return output


if __name__ == "__main__":
    output = make_expressions()
    outfile = PKGDIR / "expressions.py"
    print(f"Updating {outfile.name} ...")
    outfile.write_text(output)
