"""Generate src/mintalib/indicators.py"""

import inspect
from pathlib import Path
from pprint import pformat

PACKAGE = "mintalib"
ROOTDIR = Path(__file__).parent.parent
PKGDIR = ROOTDIR.joinpath(f"src/{PACKAGE}").resolve(strict=True)

from mintalib import core
from mintalib.builder import annotate_parameter

PRELUDE = '''"""
Indicators offer a composable interface where a calculation routine is bound with its parameters.

An indicator instance is a callable and can be applied to prices or series data as if it were a function e.g. `SMA(50)(prices)`.

Indicators support the `|` operator to apply them to data e.g. `prices | SMA(50)` or to chain them together e.g. `EMA(20) | ROC(1)`.
"""

# Do not edit! This file was generated.

from mintalib import core
from mintalib.model.indicator import wrap_indicator

'''


def make_signature(calc_func):
    sig = inspect.signature(calc_func)
    first_param = next(iter(sig.parameters.values()))

    new_params = []
    for param in sig.parameters.values():
        if param.name in ("series", "prices"):
            continue
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

    return sig.replace(parameters=new_params)


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

    xnames = pformat(fnames, width=75, compact=True, indent=4)
    xnames = xnames.replace("[", " ").replace("]", "")
    output += f"__all__ = [\n{xnames}\n]\n"

    return output


if __name__ == "__main__":
    output = make_indicators()
    outfile = PKGDIR / "indicators.py"
    print(f"Updating {outfile.name} ...")
    outfile.write_text(output)
