# Cython nogil rollout

- Why: the polars bridge (`model/expression.py` `wrap_expression`) runs each `calc_*` kernel via `map_batches`. Polars dispatches those callbacks onto its own worker threads and parallelizes independent expressions / `over` / `group_by` partitions — but without releasing the GIL the callbacks serialize on it even on separate threads. Releasing the GIL in the numeric loop is what lets that parallelism materialize. (No speedup for a single lone call; the payoff is concurrency.)
- Safe pattern: keep array creation and shape checks under GIL, then wrap pure numeric loops in `with nogil`.
- Allowed in `nogil`: libc math (`isnan`, `math.log`, `math.sqrt`, `math.fabs`), memoryview reads/writes, numeric comparisons/arithmetic.
- Common gotcha: replace in-loop `np.nan` with C-level `NAN` constant before adding `with nogil`.
- Verify via `uv run pytest` (compilation + runtime parity).
