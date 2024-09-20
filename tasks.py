# noinspection PyUnresolvedReferences

from pathlib import Path
from invoke import task  # type: ignore

PACKAGE = "mintalib"
FOLDER = Path(__file__).parent


@task
def info(c):
    """Check package versions"""
    c.run(f"pip index versions {PACKAGE}")


@task
def clean(c):
    """Remove dist folder"""
    c.run("rm -rf dist")


@task
def check(c):
    """Check package"""
    c.run("pip install -q ruff nbcheck")
    c.run("nbcheck examples misc")
    c.run("ruff check")


@task(clean)
def build(c):
    """Build project wheel"""
    c.run("pip install -q build")
    c.run("python -mbuild --sdist")


@task
def dump(c):
    """Dump wheel contents"""
    for file in FOLDER.glob("dist/*.tar.gz"):
        c.run(f"tar -tf {file}")


@task
def publish(c):
    """Publish to PyPI with twine"""
    c.run("pip install -q twine")
    c.run("twine upload dist/*.whl")
