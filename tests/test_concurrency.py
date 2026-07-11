"""Concurrency / free-threading safety checks for the core kernels.

The ``calc_*`` kernels release the GIL (``with nogil``), so threads run their
C loops concurrently even on a standard build. Computing every kernel from many
threads at once and comparing against a single-threaded reference exercises those
concurrent paths and would surface any shared-mutable-state race. This also doubles
as a regression guard for the ``freethreading_compatible`` declaration on
``core.pyx``; run the suite under a free-threaded interpreter to fully validate it.
"""

from concurrent.futures import ThreadPoolExecutor
from importlib.util import find_spec

import numpy as np
import pytest

from mintalib import core
from mintalib.samples import sample_prices
from mintalib.testing import first_param, sample_params

from test_core import list_core_functions


def equal(a, b):
    """Compare two kernel results (ndarray or namedtuple of ndarrays)."""
    if isinstance(a, tuple):
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return np.array_equal(np.asarray(a), np.asarray(b), equal_nan=True)


@pytest.fixture(scope="module")
def prices():
    backend = "pandas" if find_spec("pandas") else "polars"
    return sample_prices(backend=backend)


def test_core_concurrent(prices):
    names = list_core_functions()

    jobs = []
    for name in names:
        func = getattr(core, name)
        kwds = sample_params(func)
        data = prices["close"] if first_param(func) == "series" else prices
        jobs.append((name, func, data, kwds))

    # single-threaded reference
    reference = {name: func(data, **kwds) for name, func, data, kwds in jobs}

    def run(job):
        name, func, data, kwds = job
        return name, func(data, **kwds)

    # hammer every kernel concurrently, many rounds, sharing input buffers
    rounds = [job for _ in range(50) for job in jobs]
    with ThreadPoolExecutor(max_workers=16) as executor:
        for name, result in executor.map(run, rounds):
            assert equal(result, reference[name]), f"{name}: concurrent result != serial reference"
