# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [SemVer](https://semver.org/).

## [Unreleased]

### Added

- Community files: README, SECURITY, CONTRIBUTING, GOVERNANCE, CODE_OF_CONDUCT, ROADMAP, LICENSE (Apache-2.0).
- Repository configuration: `.editorconfig`, `.gitattributes`, `.gitignore`, `.yamllint`, `.markdownlint.yaml`, pre-commit hooks, Renovate.
- Issue and pull request templates, CODEOWNERS.
- MkDocs Material site configuration with strict validation and a hash-locked `requirements-docs` lock file.
- `sources.yaml` and `tools/aggregate.py`: copies pinned `docs/` of platform repositories, rewrites links that leave `docs/`, generates `mkdocs.generated.yml`; unit tests in `tests/`.
- Renovate: `git-refs` updates of pinned repositories in `sources.yaml`.
- ADR 0001: aggregate repository docs via CI copy.
- Platform ADRs 0002–0022 (status `proposed`).
- Runbooks, incident response, threat models, postmortems and exercises: index pages and templates.
- Repository documentation in `docs/about/`: getting started, setup, configuration, usage, operations, architecture, security, troubleshooting, reference.
- Cross-cutting pages: platform overview, principles, cluster constructor, deploy everything, network, security, compliance, capacity.
