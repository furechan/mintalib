# Polars expression interface

`mintalib.expressions` is a public interface alongside `mintalib.functions` and
`mintalib.indicators`. Mintalib invested in equivalent indicator coverage across
eager NumPy/pandas/polars calculations, composable pandas indicators, and native
Polars expressions; the public documentation should make that equivalence clear.

Bartons remains a dedicated Polars technical-analysis library, but its existence
does not make mintalib's expression surface internal. The two libraries can
coexist and provide useful independent implementations for comparison.

The expression layer serves both users and project development through:

- native Polars expression composition;
- benchmarking mintalib's Cython kernels through Polars;
- cross-checking results and semantics against Bartons; and
- investigating interoperability between eager and expression workflows.

Keep `src/mintalib/expressions.py`, its generator and model wrapper, expression
tests (including behavioral parity coverage), optional Polars dependencies,
generated API reference, and `playground/expressions.ipynb` working. Treat
expressions as a supported public surface with the same core calculation
coverage as functions and indicators.
