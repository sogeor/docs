# Usage

Typical changes. Each one ends with the local checks from [Getting started](getting-started.md#verify).

## Add or change a cross-cutting page

1. Edit or create a page in `docs/`.
2. Add a new page to `nav` in `mkdocs.yml`; the strict build fails on pages outside `nav`.
3. Link the page from related pages with relative links.
4. Add a line to `CHANGELOG.md` under **Unreleased**.

## Add a platform ADR

1. Copy the structure of an existing record to `docs/adr/NNNN-<slug>.md` with the next number.
2. Set `Status: proposed` and the date.
3. Add the record to the table in `docs/adr/index.md` and to `nav` under **Decisions**.
4. When the maintainer accepts it, change the status to `accepted` in a separate pull request.
5. To replace a decision, set the old record to `superseded` with a link to the new one.

## Add a runbook, playbook, threat model, postmortem or exercise

1. Copy the template of the section (for example `docs/runbooks/template.md`) to a new file.
2. Replace every `CHANGE_ME`.
3. Add the page to the section table and to `nav`.

## Add a repository to the site

Prerequisites: the repository has `docs/` (and ideally `mkdocs.yml` with `nav`), and its own strict build passes.

1. Find the commit to publish (a release tag is preferred):

    ```bash
    git ls-remote https://github.com/<owner>/<repo> 'refs/tags/v1.0.0*'
    ```

2. Add an entry to `sources.yaml`:

    ```yaml
      - name: modules
        title: Modules
        url: https://github.com/<owner>/modules
        ref: v1.0.0
        sha: <40-character commit SHA from step 1; the ^{} line for an annotated tag>
    ```

3. Run `python3 tools/aggregate.py` and `mkdocs build --strict -f mkdocs.generated.yml`.
4. Update the repository status table in `docs/index.md`.

Expected: the repository appears under **Repositories**; Renovate starts tracking `ref`.

## Preview changes of another repository before they are released

```bash
python3 tools/aggregate.py --local modules=../modules
mkdocs serve -f mkdocs.generated.yml
```
