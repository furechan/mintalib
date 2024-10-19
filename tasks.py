# noinspection PyUnresolvedReferences

import re

from pathlib import Path
from invoke import task  # type: ignore

PACKAGE = "mintalib"
ROOT = Path(__file__).parent


@task
def install(ctx):
    """Install Package with extras"""
    ctx.run('python -mpip install -e ".[extras]"')


@task
def info(ctx):
    """Check package versions"""
    ctx.run(f"python -mpip index versions {PACKAGE}")


@task
def clean(ctx):
    """Cleanup and remove dist folder"""
    ctx.run("python setup.py clean")
    ctx.run("rm -rf dist")


@task
def check(ctx):
    """Check package"""
    ctx.run("python -mpip install -q ruff nbcheck")
    ctx.run("nbcheck examples misc")
    ctx.run("ruff check")


@task
def cython(ctx):
    """Cythonize *.pyx files"""
    ctx.run("python -mpip install -q cython")
    ctx.run("cythonize -f src/**/*.pyx")


@task(cython)
def make(ctx):
    """Compile extension with build_ext --inplace"""
    ctx.run("python -mpip install -q ipython")
    ctx.run("python setup.py build_ext --inplace")
    ctx.run("ipython misc/make-indicators-func.ipynb")
    ctx.run("ipython misc/make-functions.ipynb")
    ctx.run("ipython misc/update-readme.ipynb")


@task(clean)
def build(ctx):
    """Build project sdist"""
    print("Bulding sdist ... (use compile to compile extension inplace)")
    ctx.run("python -mpip install -q build")
    ctx.run("python -mbuild --sdist")


@task
def dump(ctx):
    """Dump sdist contents"""
    for file in ROOT.glob("dist/*.tar.gz"):
        ctx.run(f"tar -tf {file}")


@task
def publish(ctx):
    """Publish to PyPI with twine"""
    ctx.run("python -mpip install -q twine")
    ctx.run("twine upload dist/*.tar.gz")


@task
def bump(ctx):
    """Bump patch version in pyproject"""
    pyproject = Path(__file__).joinpath("../pyproject.toml").resolve(strict=True)
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
