"""nox configuration

Sessions install the package with uv, which caches built wheels keyed on the
source tree — the Cython extension is only recompiled when core.c changes.

Usage:
    uv run nox            # everyday set: tests + pandas + polars + ruff + ty
    uv run nox -t full    # full pre-publish matrix (Python 3.10-3.14, 3.13t)
    uv run nox -l         # list sessions
"""

import nox

nox.options.default_venv_backend = "uv"
nox.options.envdir = ".venv/nox"
nox.options.sessions = ["tests", "pandas", "polars", "ruff", "ty"]

PYTHON_MATRIX = ["3.10", "3.11", "3.12", "3.13", "3.14"]

ENV = {"PYTHONDONTWRITEBYTECODE": "1"}


@nox.session(tags=["full"])
def tests(session):
    """Test suite on the default interpreter with both backends"""
    session.install(".", "pytest", "pandas", "polars")
    session.run("pytest", env=ENV)


@nox.session(python=PYTHON_MATRIX, tags=["full"])
def matrix(session):
    """Test suite across supported Python versions"""
    session.install(".", "pytest", "pandas", "polars")
    session.run("pytest", env=ENV)


# free-threaded build — validates GIL-free core kernels (see tests/test_concurrency.py).
# pandas only: polars has no cp313t wheel yet and a source build OOMs.
@nox.session(python="3.13t", tags=["full"])
def freethreaded(session):
    """Test suite on free-threaded Python (pandas only)"""
    session.install(".", "pytest", "pandas")
    session.run("pytest", env=ENV)


# pandas-only install — polars tests skip via importorskip
@nox.session(tags=["full"])
def pandas(session):
    """Test suite with pandas only"""
    session.install(".", "pytest", "pandas")
    session.run("pytest", env=ENV)


# polars-only install — pandas tests skip via skipif
@nox.session(tags=["full"])
def polars(session):
    """Test suite with polars only"""
    session.install(".", "pytest", "polars")
    session.run("pytest", env=ENV)


@nox.session(tags=["full"])
def ruff(session):
    """Lint with ruff"""
    session.install("ruff")
    session.run("ruff", "check", "src", "tests")


@nox.session(tags=["full"])
def ty(session):
    """Type check with ty"""
    session.install(".", "ty", "pandas", "polars")
    session.run("ty", "check", "src/mintalib")
