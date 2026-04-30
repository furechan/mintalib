---
name: pandas expressions (pd.col)
description: pandas 3.0 Expression API — pd.col, pandas.api.typing.Expression, operator support, constructor
type: reference
---

`pandas.api.typing.Expression` — introduced in pandas 3.0 (requires Python 3.11+).

**Source:** `pandas/core/col.py`

**Constructor:** `Expression(func, repr_str, needs_parenthese=False)`
- `func` — any `(DataFrame) -> Any` callable
- `repr_str` — string label used in `repr()` and operator composition

**`pd.col("close")`** — factory that returns an `Expression` wrapping `lambda df: df["close"]`.

**Operators** — all Python operators overloaded (`<`, `>`, `<=`, `>=`, `==`, `!=`, `+`, `-`, `*`, `/`, `&`, `|`, `^`, `~`, `**`, `%`, unary `-`/`+`/`abs`). Each returns a new `Expression`. Also supports `__array_ufunc__` and `__getattr__` (deferred attribute access).

**Evaluation:** `expr._eval_expression(df)` — private but works. pandas calls it internally in `df.__getitem__`, `df.assign()`, `df.loc[]`.

**Usage:**
```python
df.assign(flag=pd.col("close") < 30)
df.loc[pd.col("close") > 25]
df[pd.col("close") < 30]
```

**Key limitation:** no public `.map()` / `.map_batches()` — cannot attach arbitrary computations via the public API. Must subclass or pass a custom `func` directly to `Expression(func, repr_str)`.

**In mintalib:** project pinned to Python 3.11 (`.python-version`) so pandas 3.0.2 is available. Used for the `as_expr()` bridge on `Indicator` — see `docs/indicator-bridge-proposal.md`.
