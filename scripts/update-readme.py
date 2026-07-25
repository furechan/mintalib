"""Update README.md indicators table"""

import re
import inspect

from pathlib import Path

import pandas as pd

ROOTDIR = Path(__file__).parent.parent


def get_input(name):
    """Input type (Prices/Series) from the core function's first parameter"""
    from mintalib import core

    func = getattr(core, f"calc_{name.lower()}", None) or getattr(
        core, f"flag_{name.lower()}", None
    )
    if func is None:
        return "Prices"  # EVAL has no core function, evaluates against prices
    param = next(iter(inspect.signature(func).parameters), "")
    return param.capitalize()


def get_info(func):
    info = dict(Name=func.__name__)
    doc = func.__doc__ or ""
    lines = [l.strip() for l in doc.strip().splitlines() if l.strip()]
    if lines and lines[0].startswith(("calc_", "flag_")):
        lines = lines[1:]
    description = lines[0] if lines else ""
    info.update(Input=get_input(func.__name__))
    if description:
        info.update(Description=description)
    return info


def list_indicators():
    from mintalib import indicators

    result = [v for k, v in vars(indicators).items() if k.isupper() and callable(v)]
    result = [get_info(f) for f in result]
    result = pd.DataFrame(result).set_index("Name")
    result = result.sort_index()
    return result


def update_readme(verbose=True):
    title = "## List of Indicators\n"
    table = list_indicators().to_markdown()
    repl = title + "\n" + table + "\n\n\n"

    pattern = r"(?ms)(^[#]+ List of (Functions|Indicators)\n[^#]+)"

    readme = ROOTDIR.joinpath("README.md")
    contents = readme.read_text()

    output, count = re.subn(pattern, repl, contents)

    if count != 1:
        raise RuntimeError("Could not locate list of indicators")

    if verbose:
        print(f"Updating {readme.name} ...")

    readme.write_text(output)


if __name__ == "__main__":
    update_readme()
