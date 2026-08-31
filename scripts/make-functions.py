"""Generate src/mintalib/functions.py"""

import inspect
from pathlib import Path

from mintalib import core
from mintalib.builder import annotate_parameter

PACKAGE = "mintalib"
ROOTDIR = Path(__file__).parent.parent
PKGDIR = ROOTDIR.joinpath(f"src/{PACKAGE}").resolve(strict=True)

PRELUDE = '''"""
Calculation functions for technical analysis indicators.

These functions are thin wrappers around core calculation routines that handle input and output type conversion.

The function names are all lower case like `sma`, `ema`, etc.
Some names like `abs`, `min`, `max`, `sum` shadow Python builtins.
It is advised to import the module with a short alias rather than importing names directly:

```python
import mintalib.functions as ta
```
"""

# Do not edit! This file was generated.

from mintalib import core

'''


def wrapper_name(calc_func):
    first_param = next(iter(inspect.signature(calc_func).parameters))
    if first_param == "series":
        return "wrap_series_function"
    return "wrap_columns_function"

def make_signature(calc_func):
    sig = inspect.signature(calc_func)
    new_params = []
    params = list(sig.parameters.values())
    inputs = getattr(calc_func, "metadata", {}).get("inputs")

    if inputs:
        new_params.extend(params[: len(inputs)])
        params = params[len(inputs):]

    for param in params:
        param = annotate_parameter(param)
        new_params.append(param)
    return sig.replace(parameters=new_params)


def make_function(calc_func, name=None):
    if name is None:
        name = calc_func.__name__.removeprefix("calc_").lower()
    cname = f"core.{calc_func.__name__}"
    signature = make_signature(calc_func)
    decorator = wrapper_name(calc_func)
    buffer = f"@{decorator}({cname})\n"
    buffer += f"def {name}{signature}: ...\n"
    return buffer


def core_functions():
    return sorted(k for k, v in vars(core).items() if k.startswith("calc_") and callable(v))


def make_functions(cnames=None):
    if cnames is None:
        cnames = core_functions()

    funcs = [getattr(core, cname) for cname in cnames]
    wrappers = sorted({wrapper_name(func) for func in funcs})
    imports = "from mintalib.model.function import (\n"
    imports += "".join(f"    {wrapper},\n" for wrapper in wrappers)
    imports += ")\n\n"
    output = PRELUDE + imports

    for cname, func in zip(cnames, funcs):
        name = cname.removeprefix("calc_").lower()
        code = make_function(func, name)
        output += code + "\n"

    return output


if __name__ == "__main__":
    output = make_functions()
    outfile = PKGDIR / "functions.py"
    print(f"Updating {outfile.name} ...")
    outfile.write_text(output)
