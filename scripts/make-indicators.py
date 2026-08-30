"""Generate src/mintalib/indicators.py"""

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
Indicators offer a composable interface where a calculation routine is bound with its parameters.

This module is pandas-only: indicators accept pandas DataFrames, pandas Series, or numpy arrays,
and return pandas results.

An indicator instance is a callable applied to prices or series data: `SMA(50)(prices)`.

Series-output indicators chain through the `|` operator: `EMA(20) | ROC(1)`.

Single-output indicators return a pandas Series; multi-output indicators (e.g. `MACD`, `BBANDS`) return a DataFrame.
Select one output of a multi-output indicator as a series indicator with `MACD()["macd"]`.
"""

# Do not edit! This file was generated.
from mintalib import core
from mintalib.model.indicator import (
    EVAL,
    PricesToFrame,
    PricesToSeries,
    SeriesToFrame,
    SeriesToSeries,
    wrap_indicator,
)

'''


def make_signature(calc_func):
    sig = inspect.signature(calc_func)
    params = list(sig.parameters.values())
    first_param = params[0]
    inputs = tuple(getattr(calc_func, "metadata", {}).get("inputs", ()))

    if first_param.name == "series":
        params = params[1:]
    elif first_param.name == "prices":
        params = params[1:]
    elif inputs and tuple(param.name for param in params[: len(inputs)]) == inputs:
        params = params[len(inputs):]
    else:
        raise ValueError(f"Cannot determine inputs for {calc_func.__name__!r}")

    new_params = []
    for param in params:
        param = annotate_parameter(param)
        new_params.append(param)

    if first_param.name == "series":
        item_param = inspect.Parameter(
            name="item",
            kind=inspect.Parameter.KEYWORD_ONLY,
            default=None,
            annotation=str | None,
        )
        new_params.append(item_param)

    metadata = getattr(calc_func, "metadata", {})
    input_name = "Series" if first_param.name == "series" else "Prices"
    output_name = "Frame" if metadata.get("output_names") else "Series"
    return sig.replace(
        parameters=new_params,
        return_annotation=Symbol(f"{input_name}To{output_name}"),
    )


class Symbol(str):
    def __repr__(self):
        return self


def make_indicator(calc_func, name=None):
    if name is None:
        name = calc_func.__name__.removeprefix("calc_").upper()
    cname = f"core.{calc_func.__name__}"
    newsig = make_signature(calc_func)
    buffer = f"@wrap_indicator({cname})\n"
    buffer += f"def {name}{newsig}: ...\n"
    return buffer


def core_functions():
    return sorted(k for k, v in vars(core).items() if k.startswith("calc_") and callable(v))


def make_indicators(cnames=None):
    if cnames is None:
        cnames = core_functions()

    output = PRELUDE + "\n\n"

    fnames = []

    for cname in cnames:
        cfunc = getattr(core, cname)
        name = cname.removeprefix("calc_").upper()
        code = make_indicator(cfunc, name)
        fnames.append(name)
        output += code + "\n"

    fnames.append("EVAL")
    fnames.sort()

    xnames = pformat(fnames, width=75, compact=True, indent=4)
    xnames = xnames.replace("[", " ").replace("]", "")
    output += f"__all__ = [\n{xnames}\n]\n"

    return output


if __name__ == "__main__":
    output = make_indicators()
    outfile = PKGDIR / "indicators.py"
    print(f"Updating {outfile.name} ...")
    outfile.write_text(output)
