# Troubleshooting

## `Aborted with N warnings in strict mode!`

| Warning | Cause | Fix |
|---|---|---|
| `pages exist in the docs directory, but are not included in the "nav"` mentioning `repos/` | Built with `mkdocs.yml` after aggregation | Build with `-f mkdocs.generated.yml`, or remove `docs/repos/` |
| same, for your page | New page not added to `nav` | Add it to `nav` in `mkdocs.yml` |
| `contains a link '…', but the target '…' is not found` | Broken relative link | Fix the path; links are relative to the page |
| `contains a link '…#anchor', but there is no such anchor` | Heading renamed | Use the anchor MkDocs generates: lowercase, spaces to `-` |
| warning inside `repos/<name>/` | The aggregated repository has a broken page at that SHA | Fix it in that repository, then update the pin |

## `error: <name>: docs/<page> links outside the repository`

**Cause:** a page links to `../../…` beyond the repository root.
**Fix:** use a full URL in the source repository.

## `error: <name>: fetched <sha>, expected <sha>`

**Cause:** the commit is not reachable or `sha` is wrong.
**Fix:** check `git ls-remote <url>` and copy the full SHA.

## `fatal: … couldn't find remote ref` or `CalledProcessError` during fetch

**Cause:** wrong `url`, private repository, or no network.
**Fix:** open the URL in a browser; use `--offline` with an existing cache or `--local NAME=PATH`.

## `error: <name>: not in cache; run without --offline first`

**Cause:** `--offline` without a previous online run.
**Fix:** run `python3 tools/aggregate.py` once with network access.

## `ERROR: Hashes are required in --require-hashes mode`

**Cause:** the lock file was edited by hand or generated without `--generate-hashes`.
**Fix:** regenerate it as described in [Operations](operations.md#update-locked-python-dependencies).

## Renovate does not update `sources.yaml`

**Cause:** the entry does not match the expected order `url`, `ref`, `sha` on consecutive lines.
**Fix:** keep the key order from [Configuration](configuration.md#sourcesyaml).

## Pages deployment fails with `Branch "…" is not allowed to deploy to github-pages`

**Cause:** the environment allows only `master`.
**Fix:** run the workflow on `master`; pull requests only build.
