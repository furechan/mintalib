# Internal Polars expression bridge

`mintalib.expressions` is intentionally retained but no longer advertised as a
primary public interface. Bartons is the dedicated Polars technical-analysis
library; mintalib is positioned around eager NumPy/pandas functions, with
composable pandas indicators as a secondary interface. The module remains
importable for internal comparison work, but carries no public API stability
guarantee.

The expression layer remains useful internally for:

- benchmarking mintalib's Cython kernels through Polars;
- cross-checking results and semantics against Bartons;
- investigating interoperability and migration paths; and
- providing a temporary internal bridge while the libraries converge.

Keep `src/mintalib/expressions.py`, its generator and model wrapper, expression
tests (including behavioral parity coverage), optional Polars dependencies, and
`playground/expressions.ipynb` working for now. Generated expression API
reference pages may remain available for inspection, but expressions should not
be promoted in the README, quick start, or example navigation.

Do not remove this layer merely because it is absent from the advertised API.
Removal should be an explicit decision made after benchmarks and Bartons parity
checks no longer depend on it, or after a generic internal adapter replaces all
of those uses.
