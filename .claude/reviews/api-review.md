# API Review — 2026-03-26

## Typos / errors in docstrings — fixed ✓

- `functions.py` module doc: "arround" → "around"
- `macd` / `macdv`: "show time period" → "short time period" (n1)
- `macd` / `macdv`: "long time periodm" → "long time period" (n2)

## `shift` vs `lag` — resolved ✓

`shift` was a numpy-style name; `lag` is the standard TA name. `shift` removed entirely.
`shift.pxi` kept in codebase but excluded from `_all_core.pxi`.

## `abs`, `min`, `max`, `sum` shadow Python builtins — fixed ✓

Module docstring now explicitly calls out the shadowing and recommends
`import mintalib.functions as ta` over importing names directly.

## `price` item abbreviations unexplained — fixed ✓

Docstring now documents all aliases. Also fixed a bug where `==` was used instead of `in`
for tuple membership checks, meaning `'ohlc4'`, `'hl2'`, `'hlc3'`, `'hlcc4'` aliases silently failed.

Source file: `src/mintalib/cython/price.pxi`

## `eval` docstring fixed ✓

`eval` works with both pandas (via `DataFrame.eval`) and polars (via `DataFrame.sql`).
The docstring incorrectly said "pandas only" — fixed in `src/mintalib/cython/eval.pxi`.
