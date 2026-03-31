# noinspection PyUnresolvedReferences
"""
Invoke tasks for mintalib development.

Setup:
    uv sync                 # install deps and compile Cython extension

Common tasks:
    inv info                # show working version
    inv make                # recompile Cython + regenerate all derived files
    inv docs                # generate Markdown documentation
    inv build               # clean → build sdist
    inv dump                # list contents of built sdist
    inv publish             # upload dist/*.tar.gz to PyPI via twine
    inv publish --testpypi  # upload to TestPyPI instead
    inv bump                # bump patch version in pyproject.toml
    inv depcheck            # upgrade packages flagged by Dependabot alerts, then sync

After editing any .pxi file, run `inv make` to recompile and regenerate all derived files.
This runs cythonize, build_ext, and all codegen notebooks (make-functions, make-indicators,
make-expressions, update-readme).

Publishing workflow (order matters — tox must pass before publishing, bump runs after):
    inv make
    inv build
    inv dump
    tox
    inv publish
    inv bump
    git add pyproject.toml && git commit -m "Bump version"

Security updates:
    inv depcheck            # fetches open Dependabot alerts, upgrades flagged packages
                            # in uv.lock, and syncs the environment; then commit uv.lock
"""

import re
import json
import subprocess

from pathlib import Path
from invoke import task  # type: ignore

PACKAGE = "mintalib"
ROOT = Path(__file__).parent


def get_version():
    """Get version from pyproject"""
    data = ROOT.joinpath("pyproject.toml").read_text()
    pattern = r"^version \s* = \s* \"(.+)\" \s*"
    match = re.search(pattern, data, flags=re.VERBOSE | re.MULTILINE)
    return match.group(1)


def bump_version():
    """Bump patch version in pyproject"""
    pyproject = ROOT.joinpath("pyproject.toml").resolve(strict=True)
    buffer = pyproject.read_text()
    pattern = r"^version \s* = \s* \"(.+)\" \s*"
    match = re.search(pattern, buffer, flags=re.VERBOSE | re.MULTILINE)
    if not match:
        raise ValueError("Could not find version setting")
    version = tuple(int(i) for i in match.group(1).split("."))
    version = version[:-1] + (version[-1] + 1,)
    version = ".".join(str(v) for v in version)
    print(f"Updating version to {version} ...")
    output = re.sub(
        pattern, f'version = "{version}"\n', buffer, flags=re.VERBOSE | re.MULTILINE
    )
    pyproject.write_text(output)


@task
def info(ctx):
    """Check package version"""
    version = get_version()
    print(f"Working version: {version}")


@task
def clean(ctx):
    """Cleanup and remove dist folder"""
    ctx.run("python setup.py clean")
    ctx.run("rm -rf dist")


@task
def check(ctx):
    """Check package"""
    ctx.run("nbcheck examples misc")
    ctx.run("ruff check")


@task
def cython(ctx):
    """Cythonize *.pyx files"""
    ctx.run("cythonize -f src/**/*.pyx")


@task(cython)
def make(ctx):
    """Compile extension with build_ext --inplace"""
    ctx.run("python setup.py build_ext --inplace")

    ctx.run("python scripts/make-stubs.py")

    with ctx.cd("scripts"):
        ctx.run("ipython make-functions.ipynb")
        ctx.run("ipython make-indicators.ipynb")
        ctx.run("ipython make-expressions.ipynb")
        ctx.run("ipython update-readme.ipynb")


@task(clean)
def build(ctx):
    """Build project sdist"""
    ctx.run("uv build --sdist")


@task
def dump(ctx):
    """Dump sdist contents"""
    for file in ROOT.glob("dist/*.tar.gz"):
        ctx.run(f"tar -tf {file}")

@task
def docs(ctx):
    """Generate Markdown documentation"""
    ctx.run("python scripts/make-docs.py")


@task
def publish(ctx, testpypi=False):
    """Publish to PyPI with twine"""
    repoarg = "--repository testpypi" if testpypi else ""
    ctx.run(f"twine upload {repoarg} --skip-existing dist/*.tar.gz")


@task
def depcheck(ctx):
    """Upgrade packages flagged by Dependabot security alerts"""
    result = subprocess.run(
        ["gh", "api", "repos/Furechan/mintalib/dependabot/alerts",
         "--jq", "[.[] | select(.state==\"open\") | .dependency.package.name]"],
        capture_output=True, text=True, check=True
    )
    packages = list(dict.fromkeys(json.loads(result.stdout)))
    if not packages:
        print("No open Dependabot alerts.")
        return
    print(f"Upgrading: {', '.join(packages)}")
    upgrade_flags = " ".join(f"--upgrade-package {p}" for p in packages)
    ctx.run(f"uv lock {upgrade_flags}")
    ctx.run("uv sync")


@task
def bump(ctx):
    """Bump project version"""
    bump_version()
