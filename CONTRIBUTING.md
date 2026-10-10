# Contributing

## Process

1. Open an [issue](https://github.com/sogeor/docs/issues) for bugs and requests
   (English or Russian). Report vulnerabilities privately per [SECURITY.md](SECURITY.md).
2. Create a branch `docs/...`, `feat/...` or `fix/...` and open a pull request to `master`.
3. Requirements for a pull request to be accepted:
   - [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) messages;
   - signed commits;
   - all required checks green (`validate`, `docs`);
   - `CHANGELOG.md` updated for user-visible changes;
   - platform-level decisions recorded as an ADR in `docs/adr/` (status `proposed`).

Documentation of a single repository lives in that repository and is aggregated into the site;
change it there, not here.

By contributing you agree that your contribution is licensed under [Apache-2.0](LICENSE).

## Tests

- Every change must pass `mkdocs build --strict`, markdownlint and lychee.
- Changes to aggregation scripts come with tests for the changed behavior.

## Writing standards

| Area | Standard | Enforced by |
|---|---|---|
| Markdown | `.markdownlint.yaml`; relative links between pages; full GitHub URLs to other repositories | `markdownlint-cli2`, `lychee`, `mkdocs build --strict` |
| Instructions | Goal → prerequisites → numbered steps with exact commands → expected result → how to verify → troubleshooting link | review |
| Examples | No personal values: `example.com`, `203.0.113.0/24` (RFC 5737), `CHANGE_ME` | `gitleaks`, review |
| ADR | [MADR](https://adr.github.io/madr/), `NNNN-title.md`, status `proposed` / `accepted` / `superseded` | review |
| Diagrams | Mermaid | `mkdocs build --strict` |
| YAML | 2-space indent, `.yamllint` | `yamllint --strict` |
| GitHub Actions | Actions pinned by full SHA with a version comment, minimal `permissions`, `persist-credentials: false` | `actionlint`, `zizmor` |

All documentation, comments and messages are in English.

## Local setup

```bash
git clone https://github.com/sogeor/docs.git
cd docs
pre-commit install
pre-commit run --all-files
```

Requires Python 3.12 and `pre-commit`.
