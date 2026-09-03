# noinspection PyUnresolvedReferences

import json
import re
import subprocess
import urllib.error
import urllib.request

from pathlib import Path

from invoke.exceptions import Exit
from invoke.tasks import task

PACKAGE = "mintalib"
ROOT = Path(__file__).parent
VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:\.dev0)?$")



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
    """Move a released patch version to the next patch development version."""
    version = get_version()
    match = VERSION_PATTERN.fullmatch(version or "")
    if version is None or match is None or version.endswith(".dev0"):
        raise Exit(f"expected a plain three-part release version, found {version!r}")
    major, minor, patch = map(int, match.groups())
    next_version = f"{major}.{minor}.{patch + 1}.dev0"
    ctx.run(f"uv version --no-sync {next_version}")
    print(f"Started development of {next_version}")


@task
def release(ctx):
    """Preflight, commit, tag, and push the current development release."""
    branch = ctx.run("git branch --show-current", hide=True).stdout.strip()
    if branch != "main":
        print(f"Nothing to release from {branch!r}; switch to main first")
        return

    dev_version = get_version()
    match = VERSION_PATTERN.fullmatch(dev_version or "")
    if dev_version is None or match is None or not dev_version.endswith(".dev0"):
        raise Exit(f"expected a three-part .dev0 version, found {dev_version!r}")
    major, minor, patch = map(int, match.groups())
    if patch == 0:
        raise Exit("automatic patch releases require a nonzero patch component")
    release_version = f"{major}.{minor}.{patch}"
    next_version = f"{major}.{minor}.{patch + 1}.dev0"
    tag = f"v{release_version}"

    ctx.run("tox -m full")

    ctx.run(f"uv version --no-sync {release_version}")
    ctx.run("git add pyproject.toml uv.lock")
    ctx.run(f'git commit -m "Release version {release_version}"')
    ctx.run(f'git tag -a {tag} -m "Release {release_version}"')
    ctx.run(f"git push origin main {tag}")

    ctx.run(f"uv version --no-sync {next_version}")
    ctx.run("git add pyproject.toml uv.lock")
    ctx.run(f'git commit -m "Start development of {next_version}"')
    ctx.run("git push origin main")
    print(f"Pushed {tag} for release and advanced main to {next_version}")
