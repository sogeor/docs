# 0001 Aggregate repository docs via CI copy

- Status: proposed
- Date: 2026-10-10

## Context and problem statement

Each platform repository documents itself in its own `docs/` directory. The platform site must show
those pages together with cross-cutting pages, at versions that were reviewed, and must build with
`mkdocs build --strict`.

## Decision drivers

- Every external input is pinned (tag or branch plus full commit SHA) and updated through a reviewed pull request.
- The strict build must not break on links that leave a repository's `docs/` directory.
- No dependency on slowly maintained MkDocs plugins; the build works with any MkDocs Material release.
- The same procedure works locally and in CI.

## Considered options

1. Copy pinned `docs/` in CI with `tools/aggregate.py`.
2. `mkdocs-multirepo-plugin` (clones repositories during the build).
3. `mkdocs-monorepo-plugin` (merges `mkdocs.yml` of directories already present).

## Decision outcome

Chosen option: "Copy pinned `docs/` in CI with `tools/aggregate.py`".

- `sources.yaml` lists each repository with `url`, `ref` and the full commit `sha`.
- `tools/aggregate.py` fetches only `docs/` and `mkdocs.yml` at that SHA (sparse, shallow), verifies the
  commit, copies the pages to `docs/repos/<name>/`, rewrites links that leave `docs/` to GitHub URLs at the
  same SHA, and writes `mkdocs.generated.yml` (inherits `mkdocs.yml`, appends each repository's own
  navigation under **Repositories**).
- Renovate updates `sha` (and `ref` when it is a tag) through the `git-refs` datasource; the site is
  rebuilt and checked in the pull request.

### Consequences

- Good: reproducible builds, reviewed updates, no network access from inside MkDocs, no plugin lock-in.
- Good: a broken page in a repository fails this repository's pull request, not the published site.
- Bad: link rewriting is custom code that must be maintained and tested (`tests/test_aggregate.py`).
- Bad: edit links on aggregated pages are not provided; readers follow the repository link instead.

## Pros and cons of the other options

### `mkdocs-multirepo-plugin`

- Bad: fetches during the build; pinning by SHA and Renovate updates are not natural.
- Bad: compatibility with new MkDocs Material releases and strict mode is not guaranteed.

### `mkdocs-monorepo-plugin`

- Bad: still needs a separate fetch step, so it adds a dependency without removing work.
