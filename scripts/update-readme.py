"""Update README.md indicators table and generate output/pypi-readme.md"""

import re
import toml
import posixpath

from pathlib import Path

import pandas as pd

ROOTDIR = Path(__file__).parent.parent
PYPROJECT = ROOTDIR.joinpath("pyproject.toml").resolve(strict=True)


def jquery(data: dict, item: str, default=None):
    result = data
    for i in item.split("."):
        result = result.get(i, None)
        if result is None:
            return default
    return result


def get_project_url(pyproject=PYPROJECT):
    config = toml.load(pyproject)
    return jquery(config, "project.urls.homepage")


def get_info(func):
    info = dict(Name=func.__name__)
    doc = func.__doc__ or ""
    lines = [l.strip() for l in doc.strip().splitlines() if l.strip()]
    if lines and lines[0].startswith(("calc_", "flag_")):
        lines = lines[1:]
    description = lines[0] if lines else ""
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


def process_readme(file, *, project_url=None, branch="main", verbose=True):
    if project_url is None:
        project_url = get_project_url()

    def replace(m):
        exclam, alt, url = m.groups()
        ftype = "raw" if exclam else "blob"
        if url.startswith("/"):
            url = url.removeprefix("/")
            url = posixpath.join(project_url, ftype, branch, url)
            text = f"{exclam}[{alt}]({url})"
            if verbose:
                print("mapping", m.group(0), "->", text)
        else:
            text = m.group(0)
        return text

    source = file.read_text()
    return re.sub(
        r"(\!?) \[ ([^]]*) \] \( ([^)]+) \)", replace, source,
        flags=re.VERBOSE,
    )


if __name__ == "__main__":
    update_readme()

    README = ROOTDIR.joinpath("README.md").resolve(strict=True)
    OUTDIR = ROOTDIR / "output"
    OUTDIR.mkdir(exist_ok=True)

    output = process_readme(README, verbose=True)
    outfile = OUTDIR.joinpath("pypi-readme.md").resolve()
    print(f"Updating {outfile.name} ...")
    outfile.write_text(output)
