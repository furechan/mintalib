# noinspection PyUnresolvedReferences

import os
import re
import json
import subprocess

from pathlib import Path
from invoke import task

PACKAGE = "mintalib"
ROOT = Path(__file__).parent


def load_direnv(path: str | Path = ROOT):
    """Load direnv environment for `path` in os.environ. Requires direnv installed."""
    output = subprocess.check_output(
        ["direnv", "export", "json"],
        cwd=path,
        text=True
        )
    if output:
        data = json.loads(output)
        for k, v in data.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


load_direnv()


def get_version() -> str | None:
    """Get version from pyproject"""
    data = ROOT.joinpath("pyproject.toml").read_text()
    pattern = r"^version \s* = \s* \"(.+)\" \s*"
    match = re.search(pattern, data, flags=re.VERBOSE | re.MULTILINE)
    return match.group(1) if match else None


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
    ctx.run("python scripts/make-functions.py")
    ctx.run("python scripts/make-indicators.py")
    ctx.run("python scripts/make-expressions.py")
    ctx.run("python scripts/update-readme.py")


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
    ctx.run("python scripts/make-api-docs.py")


@task
def publish(ctx, testpypi=False):
    """Publish to PyPI with twine"""
    repoarg = "--repository testpypi" if testpypi else ""
    ctx.run(f"twine upload {repoarg} --skip-existing dist/*.tar.gz")


@task
def depcheck(ctx):
    """Upgrade packages flagged by dependabot security alerts"""
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
