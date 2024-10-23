# cython: language_level=3, binding=True

"""
Mintalib Core

Calculation routines implemented in cython.

Routines are typically named `calc_` followed by an indicator name all in lower caps as in `calc_sma`.

The first parameter `series` or `prices` indicates whether the calculation accepts a single series or a prices dataframe.

A `prices` dataframe should contain the columns `open`, `high`, `low`, `close` and optionally `volume` all in **lower case**.

The `wrap` parameter dictates whether to wrap the calculation result to match the type of the inputs.
When set to True, pandas inputs will yield a pandas output with an identical index.
"""

include "cython/_all_core.pxi"

__all__ = tuple(
    k for k, v in globals().items()
        if k.islower() and callable(v)
        and v.__module__.endswith(".core")
        and not isinstance(v, type)
)

