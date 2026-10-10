# Operations

## Update a pinned repository

Renovate opens a pull request **chore(deps): update aggregated docs** that changes `sha` (and `ref` for tags)
in `sources.yaml`.

1. Open the pull request and wait for the `docs` check.
2. If `docs` fails, the new pages of that repository break the strict build here: fix the repository, or
   keep the old pin and close the pull request.
3. Squash and merge; `pages` publishes the site.

Manual update without Renovate:

```bash
git ls-remote https://github.com/sogeor/images refs/heads/master
```

Put the SHA into `sources.yaml`, run the [local checks](getting-started.md#verify), open a pull request.

## Update locked Python dependencies

Run from the repository root with Python 3.12 and pip-tools:

```bash
python3 -m piptools compile --quiet --generate-hashes --allow-unsafe --strip-extras \
  -o .github/requirements-docs.txt .github/requirements-docs.in
```

- Keep the pip-compile header: Renovate reruns the command it contains.
- Remove `--no-index` from the header if local pip configuration added it.
- Add `--upgrade` only to refresh transitive dependencies on purpose; review `git diff`.

!!! warning "MkDocs 2.x"
    Do not accept MkDocs 2.x until MkDocs Material supports it.

## Publish

Publishing happens on every push to `master` (`pages` workflow). To republish without changes:
**Actions → pages → Run workflow** on `master`.

Check: the workflow run summary links to the deployed site; **Settings → Pages** shows the last deployment time.

## Roll back the site

1. Revert the offending commit through a pull request (`git revert <sha>`), or pin the repository in
   `sources.yaml` back to the previous SHA.
2. Merge; `pages` republishes.

Previous deployments are listed in **Deployments → github-pages**; GitHub Pages has no one-click rollback.

## Rotate `SCORECARD_TOKEN`

Before the token expires, create a new one as in [Repository setup](setup.md#openssf-scorecard), update the
secret, run **Actions → scorecard**, then delete the old token.

## Clean up locally

```bash
rm -rf site docs/repos mkdocs.generated.yml .cache
```
