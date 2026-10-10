# sogeor docs

End-to-end documentation of the sogeor DevSecOps platform and the source of its documentation site.

[![validate](https://github.com/sogeor/docs/actions/workflows/validate.yml/badge.svg?branch=master)](https://github.com/sogeor/docs/actions/workflows/validate.yml)
[![docs](https://github.com/sogeor/docs/actions/workflows/docs.yml/badge.svg?branch=master)](https://github.com/sogeor/docs/actions/workflows/docs.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/sogeor/docs/badge)](https://scorecard.dev/viewer/?uri=github.com/sogeor/docs)
[![License](https://img.shields.io/github/license/sogeor/docs)](LICENSE)
[![Release](https://img.shields.io/github/v/release/sogeor/docs?include_prereleases)](https://github.com/sogeor/docs/releases)

## Overview

- Cross-cutting pages: platform overview, principles, cluster constructor, network, security, compliance, capacity.
- "Deploy everything": one guide from an empty account to a working platform.
- Platform ADRs ([MADR](https://adr.github.io/madr/)), runbooks, threat models, postmortems and exercises.
- Aggregates the `docs/` directory of every platform repository, pinned by tag and SHA.
- Builds and publishes the site to GitHub Pages: <https://sogeor.github.io/docs/>.

## How it works

```mermaid
flowchart LR
  subgraph repos[Platform repositories]
    images[sogeor/images docs/]
    other[other repositories docs/]
  end
  pages[Cross-cutting pages and ADRs]
  ci[GitHub Actions: copy pinned docs, rewrite links, mkdocs build --strict]
  site[GitHub Pages]
  images --> ci
  other --> ci
  pages --> ci
  ci --> site
```

## Quick start

```bash
git clone https://github.com/sogeor/docs.git
cd docs
pip install --require-hashes -r .github/requirements-docs.txt
mkdocs serve
```

## Documentation

The site structure, guides and reference pages are being built; see the [roadmap](ROADMAP.md).

## Versions

| Tool | Version |
|---|---|
| Python | 3.12 |
| pre-commit-hooks | 6.0.0 |
| gitleaks | 8.30.1 |
| shellcheck | 0.11.0 |
| yamllint | 1.38.0 |
| markdownlint-cli2 | 0.23.3 |
| actionlint | 1.7.12 |
| zizmor | 1.30.1 |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## License

[Apache-2.0](LICENSE)
