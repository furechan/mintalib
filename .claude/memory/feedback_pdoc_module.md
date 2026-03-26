---
name: pdoc __module__ fix
description: Why pdoc skips decorated functions and how we fixed it in mintalib
type: project
---

pdoc uses `__module__` to decide if a name is native to a module or imported. The decorators `wrap_function`, `wrap_expression`, and `wrap_indicator` create closure wrappers but didn't set `__module__`, so pdoc treated all decorated functions as imported from `mintalib.model.*` and skipped them.

Fix applied (2026-03-26): added `wrapper.__module__ = func.__module__` to all three decorators in `src/mintalib/model/`.

`polars.py` had a separate issue: `__all__` only listed the 5 constants, excluding `DataFrameCalc`, `SeriesCalc`, `ExpressionCalc`. Also `expression_method` and `accessor_method` didn't set `__name__`, `__doc__`, or `__signature__` on their wrappers. Both fixed.

**Why:** indicators.py worked despite the same decorator pattern because it has an explicit `__all__` at the bottom — pdoc documents `__all__`-listed names regardless of `__module__`.
