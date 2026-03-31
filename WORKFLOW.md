# Workflow

## Setup

```bash
uv sync
```

## Development

```bash
uv run pytest        # run tests
uv run ruff check    # lint
uv run ty check      # type check
```

## Invoke tasks

```bash
inv info             # show installed package version
inv make             # recompile Cython + regenerate all derived files
inv docs             # generate Markdown documentation
inv build            # clean → build sdist
inv dump             # list contents of built sdist
inv publish          # upload dist/*.tar.gz to PyPI via twine
inv publish --testpypi  # upload to TestPyPI instead
inv bump             # bump patch version in pyproject.toml
inv depcheck         # upgrade packages flagged by Dependabot alerts, then sync
```

## After editing .pxi files

Run `inv make` to recompile and regenerate all derived files:

```bash
inv make
```

This runs cythonize, build_ext, and all codegen notebooks (`make-functions`, `make-indicators`, `make-expressions`, `update-readme`).

## Publishing workflow

Order matters — `bump` runs *after* publishing, `tox` must pass before publishing:

```bash
inv make
inv build
inv dump
tox
inv publish
inv bump
git add pyproject.toml && git commit -m "Bump version"
```

## Security updates

Run `inv depcheck` to fetch open Dependabot alerts, upgrade the flagged packages
in `uv.lock`, and sync the environment. Review the changes, then commit `uv.lock`.

```bash
inv depcheck
git add uv.lock && git commit -m "Update dependencies to address security alerts"
```
