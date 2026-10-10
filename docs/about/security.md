# Security of this repository

The security of the platform itself is described in [Security](../security.md). This page covers the
documentation repository and its build.

## What is guaranteed

| Property | How |
|---|---|
| Aggregated content is the reviewed version | Pins by full commit SHA; the fetched `HEAD` is compared with `sha` |
| Content changes are reviewed | Every change, including pin updates, goes through a pull request with required checks |
| Build dependencies are what was reviewed | Python packages installed with `--require-hashes`; actions pinned by full SHA |
| The publishing job cannot be abused from forks | Deployment only from `master` through the `github-pages` environment |
| No secrets in the repository | gitleaks in pre-commit and CI; GitHub push protection |
| Minimal CI privileges | `permissions` per job; `persist-credentials: false` |

## What is not guaranteed

- Correctness of aggregated pages: they are reviewed in their own repositories.
- Availability of GitHub Pages.
- Protection against a compromised maintainer account (mitigated by signed commits and branch rules).

## Assurance case

| Threat | Boundary | Mitigation | CWE |
|---|---|---|---|
| A repository changes its pages after review | Other repositories → build | SHA pins, `HEAD` verification | CWE-494 |
| Malicious markup or script in an aggregated page | Build → readers | Pages come only from organization repositories listed in `sources.yaml` and reviewed there | CWE-79 |
| Link rewriting points outside the repository | Build | Links leaving the repository fail the build | CWE-22 |
| Leaked secret in a commit | Contributor → repository | gitleaks, push protection | CWE-798 |
| Workflow injection through pull request data | Pull request → CI | No untrusted expressions in `run:`; `zizmor` | CWE-78 |
| Tampered dependency | Registry → build | Hash-locked requirements, SHA-pinned actions, Renovate | CWE-829 |

Vulnerabilities are reported as described in
[SECURITY.md](https://github.com/sogeor/docs/blob/master/SECURITY.md).
