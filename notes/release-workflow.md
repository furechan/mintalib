# Release Workflow

This repository uses a tag-driven PyPI release workflow designed to be reusable in other Python projects. It separates artifact construction from publication, keeps the default branch on the next development version, and gives the first push a clear failure boundary before advancing development.

## Version lifecycle

The default branch normally carries the next patch version with the PEP 440 `.dev0` suffix. For example, after publishing `0.1.11`, `main` carries `0.1.12.dev0`.

A release produces two commits and two pushes:

```text
A  Release version 0.1.12              <- tag v0.1.12, first push
B  Start development of 0.1.13.dev0    <- main, second push
```

The first push updates `main` to commit A and pushes `v0.1.12`. The tag triggers publication CI. If this push fails, the local task stops and does not create commit B. After the first push succeeds, the task creates commit B and pushes `main` again. CI checks out the tagged release commit A, not the later development commit B.

Changelog management is independent of this mechanism. Release automation neither reads nor edits the changelog.

## Local release task

The Invoke task in `tasks.py` is run with:

```console
uv run inv release
```

Its responsibilities are deliberately small:

1. Do nothing unless the current branch is `main`.
2. Require a three-part development version such as `0.1.12.dev0`.
3. Run the full local preflight with `tox -m full`.
4. Use `uv version --no-sync 0.1.12` to update `pyproject.toml` and `uv.lock` without rebuilding the editable package.
5. Commit the plain release version and create the annotated tag `v0.1.12`.
6. Push `main` and the tag together. A failed push stops the task here.
7. Use `uv version --no-sync 0.1.13.dev0`, commit the next development version, and push `main` separately.

Git handles duplicate tags and rejected pushes. The release workflow handles validation against PyPI. Avoid duplicating those checks in the local task unless another repository has a concrete need for them.

## Build workflow

`.github/workflows/build.yml` owns all artifact construction and verification. It supports both entry points:

```yaml
on:
  workflow_call:
  workflow_dispatch:
```

`workflow_dispatch` allows an independent build at any time. `workflow_call` lets the Release workflow reuse exactly the same jobs without copying their configuration.

For mintalib, Build creates and smoke-tests five `cp311-abi3` wheels and one source distribution, uploads each result as a workflow artifact, downloads the complete set in a verification job, and checks the expected artifact counts. Adapt the matrix and artifact counts to the target project.

An independently dispatched Build is only a confidence check. A release calls Build again from the tagged commit so the published artifacts are built from the exact immutable source revision being released.

## Release workflow

`.github/workflows/release.yml` triggers on version-tag pushes:

```yaml
on:
  push:
    tags:
      - "v*"
```

The workflow has three stages:

1. Validate that the tag equals `v` plus the plain three-part version in `pyproject.toml`, and that the version does not already exist on PyPI.
2. Call the reusable Build workflow and require it to succeed.
3. Download the verified artifacts and publish them with `uv publish` through PyPI Trusted Publishing.

Only the publish job receives `id-token: write`. Other jobs use read-only repository permissions. The repository and PyPI project must have Trusted Publishing configured for the workflow and its `pypi` environment.

## Manual approval

Declaring an environment in YAML does not itself create an approval gate:

```yaml
environment:
  name: pypi
```

The workflow pauses only if the GitHub `pypi` environment has a required-reviewer protection rule configured under repository settings. Without that rule, publication begins automatically after Build succeeds. If the release owner needs to approve their own runs, do not enable the environment option that prevents self-review.

## Replication checklist

- Copy and adapt `.github/workflows/build.yml`.
- Copy `.github/workflows/release.yml` and change the package name used in the PyPI validation URL.
- Adapt the wheel matrix, test commands, and verified artifact counts.
- Configure PyPI Trusted Publishing for the repository, workflow, and environment.
- Configure a required reviewer on the GitHub environment if manual approval is desired.
- Add or adapt the Invoke `release` task and its patch-version parser.
- Initialize the repository at the next `X.Y.Z.dev0` version with `uv version --no-sync`.
- Ensure the full local preflight command matches the repository's supported interpreter and backend matrix.
- Keep changelog policy separate and document it according to that repository's conventions.
