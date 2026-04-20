---
name: uv-managed project — always use uv run
description: mintalib is uv-managed; never invoke python, pytest, ruff, tox, or inv directly
type: feedback
---

Always use `uv run <cmd>` for all commands in this project. Never invoke `python`, `pytest`, `ruff`, `ty`, `tox`, or `inv` directly.

**Why:** The project is uv-managed; bare commands may hit the wrong Python or miss the editable install of mintalib. `uv run` ensures the correct venv.

**How to apply:** Prefix every shell command with `uv run` — e.g. `uv run pytest`, `uv run inv make`, `uv run tox`, `uv run python -c "..."`. Use `uv add --dev <pkg>` (not `pip install`) to add dependencies.
