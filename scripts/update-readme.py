"""Update the README.md function reference."""

import re
import inspect

from pathlib import Path

ROOTDIR = Path(__file__).parent.parent


def get_signature(func):
    """Return the public call signature without type annotations."""
    signature = inspect.signature(func)
    parameters = [
        parameter.replace(annotation=inspect.Parameter.empty)
        for parameter in signature.parameters.values()
    ]
    return signature.replace(
        parameters=parameters, return_annotation=inspect.Signature.empty
    )


def get_info(func):
    doc = func.__doc__ or ""
    lines = [line.strip() for line in doc.strip().splitlines() if line.strip()]
    if lines and lines[0].startswith(("calc_", "flag_")):
        lines = lines[1:]
    description = lines[0] if lines else ""
    api = f"`{func.__name__}{get_signature(func)}`"
    return api, description


def list_functions():
    from mintalib import functions

    result = [
        value
        for value in vars(functions).values()
        if callable(value) and value.__module__ == functions.__name__
    ]
    result = [get_info(f) for f in result]
    return sorted(result)


def make_table():
    rows = ["| | |", "|---|---|"]
    rows.extend(f"| {api} | {description} |" for api, description in list_functions())
    return "\n".join(rows)


def update_readme(verbose=True):
    title = "## Function Reference\n"
    table = make_table()
    repl = (
        title
        + "\n<!-- functions:start -->\n"
        + table
        + "\n<!-- functions:end -->\n\n\n"
    )

    pattern = r"(?ms)(^[#]+ (Function Reference|List of (Functions|Indicators))\n[^#]+)"

    readme = ROOTDIR.joinpath("README.md")
    contents = readme.read_text()

    output, count = re.subn(pattern, repl, contents)

    if count != 1:
        raise RuntimeError("Could not locate function reference")

    if verbose:
        print(f"Updating {readme.name} ...")

    readme.write_text(output)


if __name__ == "__main__":
    update_readme()
