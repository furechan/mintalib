# noinspection PyUnresolvedReferences

from pathlib import Path
from invoke import task  # type: ignore

PACKAGE = "mintalib"
ROOT = Path(__file__).parent


@task
def install(ctx):
    """Install Package with extras"""
    ctx.run("python -mpip install -e \".[extras]\"")


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
    ctx.run("ipython misc/make-functions.ipynb")
    ctx.run("ipython misc/make-indicators.ipynb")
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
