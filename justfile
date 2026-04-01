# version: 1

# Project root = where this justfile lives
root := justfile_directory()

# Default: list commands
default:
    just --list

# ---- Core runner ----
# Always:
# 1) load direnv from project root
# 2) run inside uv environment
run +args:
    direnv exec {{root}} uv run {{args}}

# ---- Common shortcuts ----

# Python
py +args:
    just run python {{args}}

# Tests
test:
    just run pytest

# Lint / format
lint:
    just run ruff check .

format:
    just run ruff format .

