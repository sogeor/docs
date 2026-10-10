# Aggregation tool

`tools/aggregate.py` — aggregate `docs/` of platform repositories into this site.

## Synopsis

```text
python3 tools/aggregate.py [--local NAME=PATH]... [--offline]
```

## Options

| Option | Description |
|---|---|
| `--local NAME=PATH` | Use the working copy at `PATH` for repository `NAME`; repeatable; `NAME` must exist in `sources.yaml` |
| `--offline` | Do not fetch; use `.cache/sources/<name>` |
| `-h`, `--help` | Show help |

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Validation, fetch or rewrite error; message on stderr starting with `error:` |

## Files

| Path | Read / written | Description |
|---|---|---|
| `sources.yaml` | read | Pinned repositories |
| `mkdocs.yml` | read | Base `nav` |
| `.cache/sources/<name>/` | written | Sparse checkout of `docs/` and `mkdocs.yml` at `sha` |
| `docs/repos/<name>/` | written | Copied and rewritten pages |
| `mkdocs.generated.yml` | written | Build configuration |

## Tests

```bash
python3 -m unittest discover -s tests -v
```
