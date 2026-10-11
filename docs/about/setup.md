# Repository setup

How to set up this repository (or your fork) so that checks, publishing, dependency updates and security
features work. Steps are in order; each ends with a check.

!!! note "Placeholders"
    `<owner>` is your GitHub organization or user. Replace it with your value.

## Repository settings

### About

**Repository → ⚙ next to About** (right column on the main page):

| Field | Value |
|---|---|
| Description | `Documentation of the sogeor DevSecOps platform: overview, cluster constructor, network, security and compliance, platform ADRs, runbooks and threat models, with pinned docs of every platform repository built into one MkDocs site.` |
| Website | `https://<owner>.github.io/docs/` (later the custom documentation domain) |
| Topics | `documentation` `mkdocs` `mkdocs-material` `github-pages` `devsecops` `platform-engineering` `architecture-decision-records` `adr` `runbooks` `threat-modeling` `kubernetes` `gitops` `infrastructure-as-code` `supply-chain-security` `compliance` |
| Include in the home page | Releases — off until the first release; Deployments — on; Packages — off |

When typing topics, finish each with **Space**: Enter picks the highlighted suggestion instead.

### Pull requests

**Settings → General → Pull Requests:**

- Allow merge commits — off; Allow squash merging — on; Allow rebase merging — off.
- Automatically delete head branches — on.

### Branch ruleset

**Settings → Rules → Rulesets → New ruleset → New branch ruleset:**

| Setting | Value |
|---|---|
| Ruleset Name | `master` |
| Enforcement status | Active |
| Bypass list | **Add bypass → Repository admin**, mode **For pull requests only** |
| Target branches | **Add target → Include default branch** |
| Restrict deletions | on |
| Require signed commits | on |
| Require a pull request before merging | on, Required approvals `0` |
| Require status checks to pass | on, **Require branches to be up to date**; checks `linters`, `tests`, `docs / docs`, `site` |
| Block force pushes | on |

Status checks appear in **Add checks** only after they have run at least once.

Check: a direct `git push` to `master` is rejected with `GH013: Repository rule violations`.

### Advanced Security

**Settings → Advanced Security:**

| Feature | Setting |
|---|---|
| Private vulnerability reporting | Enable; Require a CWE — off; Daily advisory limit — 10 |
| Dependency graph | On |
| Dependabot alerts | On |
| Malware alerts | On |
| Dependabot security updates, version updates | Off — Renovate updates dependencies |
| CodeQL analysis | **Set up → Default** (analyzes GitHub Actions workflows and Python) |
| Code quality | Off |
| Secret Protection | Enable, then **Push protection → Enable** |

Check: the **Security** tab shows **Report a vulnerability**.

## GitHub Pages

1. **Settings → Pages → Build and deployment → Source:** **GitHub Actions**.
2. **Settings → Environments → github-pages** (created automatically on the first deployment, or create it
   with **New environment**):
    - **Deployment branches and tags → Selected branches and tags → Add deployment branch or tag rule** → `master`.
    - No secrets are needed.
3. Run **Actions → pages → Run workflow** on `master`, or merge any pull request.

Check: **Settings → Pages** shows **Your site is live at `https://<owner>.github.io/docs/`**.

!!! note "Custom domain"
    A custom domain is configured later: **Settings → Pages → Custom domain**, plus a `CNAME` DNS record
    pointing to `<owner>.github.io`, and `site_url` in `mkdocs.yml`.

## Renovate

1. Install the [Renovate GitHub App](https://github.com/apps/renovate) for **Only select repositories** and
   add this repository.
2. Merge the onboarding pull request if Renovate opens one (the repository already has `renovate.json`).

Check: an issue **Dependency Dashboard** appears and lists `aggregated docs`, `github-actions`,
`python tools` and `pre-commit hooks`.

## OpenSSF Scorecard

1. Create a fine-grained personal access token: **Settings (profile) → Developer settings → Personal
   access tokens → Fine-grained tokens → Generate new token**:
    - Resource owner: `<owner>`; Repository access: this repository;
    - Repository permissions: **Administration — Read-only**;
    - Expiration: 1 year.
2. **Settings → Secrets and variables → Actions → New repository secret:** name `SCORECARD_TOKEN`, value — the token.

Check: **Actions → scorecard** succeeds and **Security → Code scanning** shows Scorecard alerts.

Scorecard alerts **Code-Review** and **Fuzzing** are expected for a single-maintainer documentation
repository: dismiss them as **Won't fix**.

## OpenSSF Best Practices

Register the repository at [bestpractices.dev](https://www.bestpractices.dev/) and add the badge to the
README. Documentation-only repositories answer **Unmet** with a justification for dynamic analysis criteria.
