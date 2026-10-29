# Backlog

Items decided or considered but not scheduled. Add new items at the end.

## General

- Review the Polars expression-construction machinery (`wrap_series_expression`, `wrap_columns_expression`, source routing, metadata, output typing, and `ExprBundle`) for a supported public authoring API that can wrap external array callables such as notebook-defined Numba kernels, potentially replacing Bearta's duplicate `kernel_expression` / factory machinery and enabling that layer to retire cleanly.
- Investigate local-clone public wrapper import failure: `uv run --no-sync python -c 'from mintalib.functions import sma, ema'` raises `ValueError: Missing inputs metadata for 'calc_adx'` in `model/function.py` while `mintalib.core.calc_sma` and `calc_ema` work; check for a stale compiled extension or metadata/code-generation mismatch, verify whether a clean rebuild resolves it, and check the published package separately (not yet tested).
