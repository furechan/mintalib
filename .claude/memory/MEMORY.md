# Memory Index

- [uv-managed project](feedback-uv-managed.md) — always use `uv run <cmd>`; never invoke python/pytest/ruff/nox/inv directly
- [pdoc __module__ fix](feedback-pdoc-module.md) — why pdoc skipped decorated functions and how we fixed it (wrap_function/expression/indicator + polars.py __all__)
- [Dual docs architecture](project-docs-architecture.md) — markdown in docs/ for AI/text, pdoc HTML via GitHub Actions for GitHub Pages
- [pandas expressions (pd.col)](reference-pandas-expressions.md) — pandas 3.0 Expression API: constructor, operator support, evaluation, key limitation (no public map), usage in mintalib as_expr() bridge
- [Cython nogil rollout](project-cython-nogil.md) — safe pattern for releasing GIL in kernel loops and common gotcha (`np.nan` in `nogil` blocks)
