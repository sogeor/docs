# Workflows

| Workflow | Triggers | Jobs (status checks) | Permissions | Secrets |
|---|---|---|---|---|
| `validate.yml` | push to `master`, pull request | `linters`: yamllint, actionlint, zizmor, gitleaks; `tests`: unit tests of the aggregation tool | `contents: read` | — |
| `docs.yml` | push to `master`, pull request | `docs`: aggregation, markdownlint, `mkdocs build --strict`, lychee | `contents: read` | — |
| `pages.yml` | push to `master`, weekly schedule, manual | `build`: aggregation and site build; `deploy`: GitHub Pages | `contents: read`; `deploy`: `pages: write`, `id-token: write` | — |
| `scorecard.yml` | push to `master`, weekly schedule, branch protection change | `analysis`: OpenSSF Scorecard | `security-events: write`, `id-token: write` | `SCORECARD_TOKEN` |

Required status checks in the ruleset: `linters`, `tests`, `docs`.
