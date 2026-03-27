---
name: synthesize
description: Regenerate .claude/output/mintalib-synthesis.md from the current state of the project
disable-model-invocation: true
argument-hint: "[output-file]"
allowed-tools: Read, Glob, Grep, Bash, Write
---

Regenerate `.claude/output/mintalib-synthesis.md` — a portable design knowledge document for mintalib, intended to be imported into related projects (e.g. barcalc) as a single context file.

The synthesis should cover:

1. **Architecture** — layer diagram (cython → core → functions/indicators/expressions), generated files, model decorators, accessors
2. **Naming conventions** — table of calc_/lower/UPPER across layers
3. **Input parameters** — `series` vs `prices` convention
4. **Multi-output indicators** — named tuples, expression structs, polars structs
5. **The four stable interfaces** — core, functions, indicators, expressions with usage examples
6. **Experimental interfaces** — pandas and polars `ts` accessors, opt-in behavior
7. **The `wrap_*` decorators** — what they do and why `__module__`/`__name__`/`__signature__` matter
8. **Code generation** — which files are generated, which notebooks generate them, `inv make`
9. **The `price` helper** — item values and aliases table
10. **Key design decisions** — decisions made and why (lag vs shift, accessor opt-in, eval polars support, etc.)
11. **Interface coverage table** — run `uv run python scripts/make-coverage.py` and embed the output

Write the result to `.claude/output/mintalib-synthesis.md`, overwriting the previous version.
