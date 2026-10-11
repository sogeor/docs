# Workflows

| Workflow | Triggers | Jobs (status checks) | Permissions | Secrets |
|---|---|---|---|---|
| `validate.yml` | push to `master`, pull request | `linters`: yamllint, actionlint, zizmor, gitleaks; `tests`: unit tests of the aggregation tool | `contents: read` | — |
| `docs.yml` | push to `master`, pull request | `docs / docs`: markdownlint, lychee, `mkdocs build --strict` of own pages (reusable workflow [`sogeor/workflows` `docs.yml`](https://github.com/sogeor/workflows/blob/master/.github/workflows/docs.yml), v0.1.1); `site`: aggregation and `mkdocs build --strict` of the whole site | `contents: read` | — |
| `pages.yml` | push to `master`, weekly schedule, manual | `build`: aggregation and site build; `deploy`: GitHub Pages | `contents: read`; `deploy`: `pages: write`, `id-token: write` | — |
| `scorecard.yml` | push to `master`, weekly schedule, branch protection change | `analysis`: OpenSSF Scorecard | `security-events: write`, `id-token: write` | `SCORECARD_TOKEN` |

Required status checks in the ruleset: `linters`, `tests`, `docs / docs`, `site`.
