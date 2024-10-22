# Minimal Technical Analysis Library for Python

The `mintalib` package contains three main modules:
- [mintalib.core](/docs/mintalib.core.md)
    low level calculation rountines implemented in cython
- [mintalib.functions](/docs/mintalib.functions.md)
    wrapper functions to compute indicators
- [mintalib.indicators](/docs/mintalib.indicators.md)
    composable interface to indicators

Most calculations are available in three flavors. The raw calculation routine is called something like
`calc_sma` and is available from the `mintalib.core` module. This is the routine implemented in cython. A function called something like `SMA` is also available from the `mintalib.functions` module, and includes facilities like selection of column (`item`) and wrapping of results. Finally an indicator with the same name `SMA` is available from the `mintalib.indicators` which offers a composable interface.

