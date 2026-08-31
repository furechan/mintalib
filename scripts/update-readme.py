"""Update the README.md indicator reference."""

import re
import inspect

import pandas as pd

from pathlib import Path

ROOTDIR = Path(__file__).parent.parent


def get_inputs(name):
    """Return the data inputs required by a core function."""
    from mintalib import core

    func = getattr(core, f"calc_{name.lower()}", None) or getattr(
        core, f"flag_{name.lower()}", None
    )
    if func is None:
        raise RuntimeError(f"Could not find a core function for {name}")

    parameter = next(iter(inspect.signature(func).parameters), "")
    if parameter == "series":
        return "series"

    inputs = getattr(func, "metadata", {}).get("inputs")
    if not inputs:
        raise RuntimeError(f"Could not determine inputs for {func.__name__}")
    return ", ".join(inputs)


def get_info(func):
    """Return the public name, input type, and summary for an indicator."""
    doc = func.__doc__ or ""
    lines = [line.strip() for line in doc.strip().splitlines() if line.strip()]
    if lines and lines[0].startswith(("calc_", "flag_")):
        lines = lines[1:]
    description = lines[0] if lines else ""
    return {
        "Name": func.__name__,
        "Data inputs": get_inputs(func.__name__),
        "Description": description,
    }


def list_indicators():
    """Return public indicators as a name-indexed DataFrame."""
    from mintalib import indicators

    values = [
        value
        for name, value in vars(indicators).items()
        if name.isupper() and callable(value)
    ]
    result = pd.DataFrame(get_info(value) for value in values).set_index("Name")
    return result.sort_index()


def update_readme(verbose=True):
    """Regenerate the indicator reference in README.md."""
    table = list_indicators().to_markdown()
    repl = (
        "## List of Indicators\n\n"
        + "<!-- indicators:start -->\n"
        + table
        + "\n<!-- indicators:end -->\n\n\n"
    )

    pattern = r"(?ms)(^[#]+ (Function Reference|List of Indicators)\n[^#]+)"

    readme = ROOTDIR.joinpath("README.md")
    contents = readme.read_text()

    output, count = re.subn(pattern, repl, contents)

    if count != 1:
        raise RuntimeError("Could not locate indicator reference")

    if verbose:
        print(f"Updating {readme.name} ...")

    readme.write_text(output)


if __name__ == "__main__":
    update_readme()
