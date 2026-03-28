"""Generate core.pyi stub file from mintalib.core using inspect.signature."""

import inspect
from pathlib import Path

from mintalib import core
from mintalib.utils import get_metadata

OUTPUT = Path(__file__).parent.parent / "src/mintalib/core.pyi"

IMPORTS = """\
from typing import Any
import numpy as np
"""


class Literal(str):
    """String that repr's without quotes, for use as inspect annotation."""
    def __repr__(self):
        return self


def make_stub(func) -> str:
    name = func.__name__
    sig = inspect.signature(func)
    output_names = get_metadata(func, "output_names")
    return_type = Literal("Any") if output_names else Literal("np.ndarray")

    new_params = []
    for param in sig.parameters.values():
        annotation = param.annotation
        # normalize string annotations like 'str'
        if isinstance(annotation, str):
            annotation = eval(annotation)
        if param.default is None and annotation is str:
            annotation = Literal("str | None")
        new_params.append(param.replace(annotation=annotation))

    new_sig = sig.replace(parameters=new_params, return_annotation=return_type)
    return f"def {name}{new_sig}: ..."


def make_stubs() -> str:
    lines = [IMPORTS]
    for name in sorted(dir(core)):
        if not name.startswith("calc_"):
            continue
        func = getattr(core, name)
        lines.append(make_stub(func))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    output = make_stubs()
    print(output)
    OUTPUT.write_text(output)
    print(f"Written {OUTPUT}")
