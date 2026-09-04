# Backlog

Items decided or considered but not scheduled. Add new items at the end.

## General

- Review the Polars expression-construction machinery (`wrap_series_expression`, `wrap_columns_expression`, source routing, metadata, output typing, and `ExprBundle`) for a supported public authoring API that can wrap external array callables such as notebook-defined Numba kernels, potentially replacing Bearta's duplicate `kernel_expression` / factory machinery and enabling that layer to retire cleanly.
