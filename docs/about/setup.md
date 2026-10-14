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
| Website | `https://docs.sogeor.com/` (in a fork: your custom domain or `https://<owner>.github.io/docs/`) |
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

### Custom domain

The reference site uses `docs.sogeor.com`. In a fork, replace `docs.example.com` with your domain.

1. In your DNS provider, create a record: type `CNAME`, name `docs`, target `<owner>.github.io`.
   In Cloudflare: **DNS → Records → Add record**, **Proxy status: DNS only** (grey cloud).
2. **Settings → Pages → Custom domain:** `docs.example.com` → **Save**. Wait for **DNS check successful**.
3. When the certificate is issued (up to an hour), enable **Enforce HTTPS**.
4. Set `site_url: https://docs.example.com/` in `mkdocs.yml` and the domain in the `lychee` exclusion of
   `.github/workflows/docs.yml`; merge the change so `pages` republishes the site.

Check: `https://docs.example.com/` opens the home page, and `https://<owner>.github.io/docs/` redirects to it.

!!! warning "Keep the record DNS only"
    With the Cloudflare proxy (orange cloud) enabled, GitHub cannot issue the certificate and
    **Enforce HTTPS** stays unavailable. See [Troubleshooting](troubleshooting.md#custom-domain-returns-404-or-https-is-unavailable).

## Renovate

1. Install the [Renovate GitHub App](https://github.com/apps/renovate) for **Only select repositories** and
   add this repository.
2. Merge the onboarding pull request if Renovate opens one (the repository already has `renovate.json`).
3. The configuration proposes a version only 7 days after it was published (`minimumReleaseAge`) to
   protect against compromised or yanked releases; security updates bypass the delay. Updates whose
   source publishes no release dates are held until the date is known.
4. Exception: pins in `sources.yaml` (group `aggregated docs`) have no delay. They point to commits of
   the organization's own repositories, the `git-refs` source has no release dates, and every pin
   update is checked by the `site` build before merge.

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
