# mintalib — type the public decorators with ParamSpec

## Problem

`mintalib.expressions`, `mintalib.functions`, and `mintalib.indicators` resolve to `Unknown` under `ty` (and other type checkers), even though the source files are statically structured with proper annotations. Only `mintalib.core` resolves cleanly, because it ships a Cython-generated `.pyi` stub.

The blocker is the decorators in `mintalib/model/`:

- `wrap_expression` in `mintalib/model/expression.py:44`
- `wrap_function` in `mintalib/model/function.py:8`
- `wrap_indicator` in `mintalib/model/indicator.py:187`

All three are untyped:

```python
def wrap_expression(calc_func):
    def decorator(func):
        ...
        return wrapper
    return decorator
```

A type checker sees `decorator: (func: Unknown) -> Unknown`, so every `@wrap_expression(...)`-annotated function loses its inner signature.

## Impact

For `ABS`, `ADX`, `BBANDS`, `SMA`, etc. (the actual public API), hover/completion in editors shows nothing useful. This is why `docs/vendor/mintalib/{expressions,functions,indicators}.md` are vendored into python-dev — the API docs are the only way to discover signatures.

If the decorators were typed, LSP would carry the full signatures and the vendored API docs could be dropped (keeping only `README.md` for narrative).

## Fix — option 1 (cheap, partial)

Declare the decorator's return type:

```python
from typing import Callable
import polars as pl

def wrap_expression(calc_func) -> Callable[[Callable], Callable[..., pl.Expr]]:
    ...
```

After this, `reveal_type(ABS)` → `Callable[..., pl.Expr]`. Recovers "callable returning `pl.Expr`" but loses parameter info (`period: int = 14` disappears from hover).

## Fix — option 2 (proper, recommended) — `ParamSpec`

`ParamSpec` captures "whatever parameters the wrapped function has" so the decorator passes them through:

```python
from typing import Callable, ParamSpec
import polars as pl

P = ParamSpec("P")

def wrap_expression(calc_func) -> Callable[[Callable[P, pl.Expr]], Callable[P, pl.Expr]]:
    ...
```

Reads as: take a function with parameters `P` returning `pl.Expr`, return a function with the same `P` and same return type. Now `reveal_type(ADX)` → `def ADX(period: int = 14, *, src: IntoExpr | None = None) -> pl.Expr` — the full original signature.

For `wrap_function` and `wrap_indicator` the return type differs (`pl.DataFrame` / `pl.Series` / an indicator class), but the shape is the same.

## Hover comparison

| Variant | Hover for `ADX` |
|---|---|
| Current (untyped) | `Unknown` |
| Option 1 (`Callable[..., pl.Expr]`) | `(*args, **kwargs) -> pl.Expr` |
| Option 2 (`ParamSpec`) | `(period: int = 14, *, src: IntoExpr \| None = None) -> pl.Expr` |

## Notes

- Runtime behaviour is unchanged — this is annotations only.
- `ParamSpec` is in `typing` since 3.10 (matches python-dev's `>= 3.10` floor).
- Applied upstream, this removes most of the rationale for `docs/vendor/mintalib/*.md` — only `README.md` would still need vendoring.
