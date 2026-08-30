# cython: language_level=3, binding=True
# cython: boundscheck=False, wraparound=False, cdivision=True, nonecheck=False
# cython: freethreading_compatible=True

"""
Calculation routines implemented in cython.

Routines are named `calc_` followed by a lower-case indicator name, as in
`calc_sma`. Kernels accept either one `series` input or explicit columns such as
`high`, `low`, `close`, and `volume`. Inputs are converted to float arrays at the
kernel boundary, and calculation parameters follow the input columns.
"""

include "cython/_all_core.pxi"

__all__ = ()
