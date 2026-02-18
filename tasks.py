# noinspection PyUnresolvedReferences

import re
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
    """Generate documentation"""
    ctx.run("pdoc mintalib -o docs")


@task
def publish(ctx, testpypi=False):
    """Publish to PyPI with twine"""
    repoarg = "--repository testpypi" if testpypi else ""
    ctx.run(f"twine upload {repoarg} dist/*.tar.gz")


@task
def bump(ctx):
    """Bump project version"""
    bump_version()
