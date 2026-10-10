# Getting started

**Goal:** build and preview the whole site, including aggregated repository pages, on your machine.

## Prerequisites

| Tool | Version | Check |
|---|---|---|
| Git | any recent | `git --version` |
| Python | 3.12 | `python3 --version` |
| pip | bundled with Python | `python3 -m pip --version` |
| Node.js (optional, for markdownlint) | LTS | `node --version` |

Network access to `github.com` and `pypi.org` is required for the first build.

## Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/sogeor/docs.git
    cd docs
    ```

2. Create a virtual environment and install the hash-locked dependencies:

    ```bash
    python3 -m venv .venv
    . .venv/bin/activate
    pip install --require-hashes -r .github/requirements-docs.txt
    ```

3. Fetch the pinned documentation of platform repositories and generate the site configuration:

    ```bash
    python3 tools/aggregate.py
    ```

    Expected output:

    ```text
    images: 40a8ff40c816 -> docs/repos/images
    wrote mkdocs.generated.yml
    ```

4. Start the preview server:

    ```bash
    mkdocs serve -f mkdocs.generated.yml
    ```

    Expected: `Serving on http://127.0.0.1:8000/`.

## Verify

Open `http://127.0.0.1:8000/`. The top navigation shows **Platform**, **Operations**, **Decisions**,
**About** and **Repositories**; **Repositories → Images** opens the aggregated `images` documentation.

Run the same checks as CI:

```bash
python3 -m unittest discover -s tests
mkdocs build --strict -f mkdocs.generated.yml
npx --yes markdownlint-cli2@0.23.3 "*.md" "docs/**/*.md" ".github/**/*.md" "#node_modules" "#docs/repos"
```

## Preview a local checkout of another repository

To see unreleased changes of a repository, point the tool at its working copy:

```bash
python3 tools/aggregate.py --local images=../images
mkdocs serve -f mkdocs.generated.yml
```

## If something goes wrong

See [Troubleshooting](troubleshooting.md).
