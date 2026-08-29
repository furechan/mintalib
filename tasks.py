# noinspection PyUnresolvedReferences

import os
import re
import json
import subprocess
import urllib.error
import urllib.request

from pathlib import Path
from invoke.exceptions import Exit
from invoke.tasks import task

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


def latest_pypi_version() -> str:
    """Get the latest published version from PyPI."""
    url = f"https://pypi.org/pypi/{PACKAGE}/json"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.load(response)["info"]["version"]
    except urllib.error.HTTPError as error:
        raise Exit(f"could not get the latest PyPI version: HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise Exit(f"could not get the latest PyPI version: {error.reason}") from error
    except (KeyError, TypeError, ValueError) as error:
        raise Exit("could not read the latest version from PyPI's response") from error


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
    """Show the current project version and the latest version on PyPI."""
    version = get_version()
    pypi_version = latest_pypi_version()
    print(f"Current version: {version}")
    print(f"Latest on PyPI: {pypi_version}")


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
    for pattern in ("core.*.so", "core.*.pyd"):
        for path in ROOT.joinpath("src/mintalib").glob(pattern):
            path.unlink()
    ctx.run("python setup.py build_ext --inplace")

    ctx.run("python scripts/make-stubs.py")
    ctx.run("python scripts/make-functions.py")
    ctx.run("python scripts/make-indicators.py")
    ctx.run("python scripts/make-expressions.py")
    ctx.run("python scripts/update-readme.py")


@task(clean)
def build(ctx):
    """Build project sdist"""
    print(
        "WARNING: inv build creates a local sdist only; "
        "publish releases through .github/workflows/release.yml."
    )
    ctx.run("python scripts/check-readme.py")
    ctx.run("uv build --sdist")


@task
def dump(ctx):
    """Dump sdist contents"""
    for file in ROOT.glob("dist/*.tar.gz"):
        ctx.run(f"tar -tf {file}")

@task
def docs(ctx, serve=False):
    """Generate Markdown API reference, optionally serve mkdocs site"""
    ctx.run("python scripts/make-api-docs.py")
    if serve:
        ctx.run("mkdocs serve")


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
