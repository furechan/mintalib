"""
tasks module (see invoke.py)

Requires:
    invoke tomli build twine
"""

import sys
import json
import tomli
import logging

from urllib import request
from urllib.error import HTTPError

from invoke import task
from pathlib import Path

from functools import lru_cache

logger = logging.getLogger()


@lru_cache
def get_python():
    return sys.executable


@lru_cache
def project_folder():
    """Load pyproject.toml file"""

    for path in Path(__file__).parents:
        if path.joinpath("pyproject.toml").exists():
            return path

    raise FileNotFoundError("pyproject.toml")


@lru_cache
def load_config():
    """Load pyproject.toml file"""

    pyproject = project_folder().joinpath("pyproject.toml").resolve(strict=True)

    with pyproject.open("rb") as f:
        return tomli.load(f)


def get_config(item, default=None):
    """Query pyproject.toml file"""

    data = load_config()

    for i in item.split("."):
        data = data.get(i, None)
        if data is None:
            return default

    return data


@task
def pwd(ctx):
    """Run pwd in project folder"""

    with ctx.cd(project_folder()):
        ctx.run("pwd")


@task
def clean(ctx):
    """Clean build and dist folders"""
    folders = ["build", "dist"]

    with ctx.cd(project_folder()):
        for folder in folders:
            ctx.run(f"rm -rf {folder}")


@task
def prune(ctx):
    """Prune non versioned folders"""
    folders = ["build", "dist", ".venv", ".nox", ".tox", "__pycache__"]

    with ctx.cd(project_folder()):
        for folder in folders:
            ctx.run(f"rm -rf {folder}")


@task(clean)
def build(ctx):
    """Build wheel with build"""
    python = get_python()
    if project_folder().joinpath("setup.py").exists():
        target = "sdist"
    else:
        target = "wheel"

    with ctx.cd(project_folder()):
        ctx.run(f"{python} -mbuild --{target}")


@task
def dump(ctx):
    """Dump wheel and sdist contents"""
    with ctx.cd(project_folder()):
        dist = Path("dist")

        for file in dist.glob("*.whl"):
            ctx.run(f"unzip -l {file}")

        for file in dist.glob("*.tar.gz"):
            ctx.run(f"tar -ztvf {file}")


@task
def publish(ctx, test_only=False):
    """Publish project with twine"""
    python = get_python()

    if test_only:
        command = f"{python} -mtwine upload --repository testpypi dist/*"
    else:
        command = f"{python} -mtwine upload dist/*"

    with ctx.cd(project_folder()):
        ctx.run(command)


@task
def info(ctx):
    """Project information"""
    name = get_config("project.name")
    version = get_config("project.version")
    print("name", name)
    print("version", version)
    print("location", project_folder())
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        res = request.urlopen(url)
        data = json.load(res)
        releases = list(data["releases"])
        print("pypi.releases", releases)
    except HTTPError:
        pass
