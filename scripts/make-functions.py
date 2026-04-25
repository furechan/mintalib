"""Generate src/mintalib/functions.py"""

import inspect
from pathlib import Path

PACKAGE = "mintalib"
ROOTDIR = Path(__file__).parent.parent
PKGDIR = ROOTDIR.joinpath(f"src/{PACKAGE}").resolve(strict=True)

from mintalib import core
from mintalib.builder import annotate_parameter

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
from mintalib.model.function import wrap_function

'''


def make_signature(calc_func):
    sig = inspect.signature(calc_func)
    new_params = []
    for param in sig.parameters.values():
        param = annotate_parameter(param)
        new_params.append(param)
    return sig.replace(parameters=new_params)


def make_function(calc_func, name=None):
    if name is None:
        name = calc_func.__name__.removeprefix("calc_").lower()
    cname = f"core.{calc_func.__name__}"
    signature = make_signature(calc_func)
    buffer = f"@wrap_function({cname})\n"
    buffer += f"def {name}{signature}: ...\n"
    return buffer


def core_functions():
    return sorted(k for k, v in vars(core).items() if k.startswith("calc_") and callable(v))


def make_functions(cnames=None):
    if cnames is None:
        cnames = core_functions()

    output = PRELUDE + "\n\n"

    for cname in cnames:
        func = getattr(core, cname)
        name = cname.removeprefix("calc_").lower()
        code = make_function(func, name)
        output += code + "\n"

    return output


if __name__ == "__main__":
    output = make_functions()
    outfile = PKGDIR / "functions.py"
    print(f"Updating {outfile.name} ...")
    outfile.write_text(output)
