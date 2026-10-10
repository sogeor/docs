#!/usr/bin/env python3
"""Aggregate docs/ of platform repositories into this site."""

from __future__ import annotations

import argparse
import posixpath
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources.yaml"
BASE_CONFIG = ROOT / "mkdocs.yml"
GENERATED_CONFIG = ROOT / "mkdocs.generated.yml"
CACHE = ROOT / ".cache" / "sources"
TARGET = ROOT / "docs" / "repos"
NAV_SECTION = "Repositories"

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
URL_RE = re.compile(r"^https://github\.com/[A-Za-z0-9-]+/[A-Za-z0-9._-]+$")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\1).)+?\1")
INLINE_LINK_RE = re.compile(r"(\]\()(<[^>]+>|[^)\s]+)((?:\s+\"[^\"]*\")?\))")
REF_DEF_RE = re.compile(r"^(\s{0,3}\[[^\]]+\]:\s*)(<[^>]+>|\S+)(.*)$")


class AggregateError(Exception):
    pass


class _IgnoreTagsLoader(yaml.SafeLoader):
    pass


_IgnoreTagsLoader.add_multi_constructor("", lambda loader, suffix, node: None)


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.load(handle, Loader=_IgnoreTagsLoader)  # noqa: S506


def load_sources(path: Path = SOURCES) -> list[dict[str, str]]:
    data = load_yaml(path) or {}
    repos = data.get("repositories") or []
    seen: set[str] = set()
    for repo in repos:
        for key in ("name", "title", "url", "ref", "sha"):
            if not isinstance(repo.get(key), str) or not repo[key]:
                raise AggregateError(f"{path.name}: repository entry is missing '{key}'.")
        if not NAME_RE.match(repo["name"]):
            raise AggregateError(f"{path.name}: invalid name '{repo['name']}'.")
        if repo["name"] in seen:
            raise AggregateError(f"{path.name}: duplicate name '{repo['name']}'.")
        if not URL_RE.match(repo["url"]):
            raise AggregateError(f"{path.name}: '{repo['name']}' url must be https://github.com/<owner>/<repo>.")
        if not SHA_RE.match(repo["sha"]):
            raise AggregateError(f"{path.name}: '{repo['name']}' sha must be a full 40-character commit SHA.")
        seen.add(repo["name"])
    return repos


def fetch(repo: dict[str, str], dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    def git(*args: str) -> str:
        result = subprocess.run(["git", "-C", str(dest), *args], check=True, capture_output=True, text=True)
        return result.stdout.strip()

    git("init", "--quiet")
    git("remote", "add", "origin", repo["url"] + ".git")
    git("sparse-checkout", "set", "--no-cone", "/docs/", "/mkdocs.yml")
    git("fetch", "--quiet", "--depth", "1", "--filter=blob:none", "origin", repo["sha"])
    git("checkout", "--quiet", "FETCH_HEAD")
    head = git("rev-parse", "HEAD")
    if head != repo["sha"]:
        raise AggregateError(f"{repo['name']}: fetched {head}, expected {repo['sha']}.")


def rewrite_target(target: str, page: str, repo: dict[str, str], source: Path) -> str:
    """Return the link target for a page copied from <source>/docs/<page>."""
    wrapped = target.startswith("<") and target.endswith(">")
    raw = target[1:-1] if wrapped else target
    if not raw or raw.startswith(("#", "/")) or SCHEME_RE.match(raw):
        return target
    path, sep, fragment = raw.partition("#")
    if not path:
        return target
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname("docs/" + page), path))
    if resolved == "docs" or resolved.startswith("docs/"):
        return target
    if resolved == ".." or resolved.startswith("../"):
        raise AggregateError(f"{repo['name']}: docs/{page} links outside the repository: {raw}")
    kind = "tree" if resolved == "." or (source / resolved).is_dir() else "blob"
    resolved = "" if resolved == "." else resolved
    url = f"{repo['url']}/{kind}/{repo['sha']}/{resolved}".rstrip("/")
    url += sep + fragment
    return f"<{url}>" if wrapped else url


def _rewrite_line(line: str, page: str, repo: dict[str, str], source: Path) -> str:
    ref = REF_DEF_RE.match(line)
    if ref:
        return ref.group(1) + rewrite_target(ref.group(2), page, repo, source) + ref.group(3)
    parts: list[str] = []
    last = 0
    for code in INLINE_CODE_RE.finditer(line):
        parts.append(_rewrite_inline(line[last:code.start()], page, repo, source))
        parts.append(code.group(0))
        last = code.end()
    parts.append(_rewrite_inline(line[last:], page, repo, source))
    return "".join(parts)


def _rewrite_inline(text: str, page: str, repo: dict[str, str], source: Path) -> str:
    return INLINE_LINK_RE.sub(
        lambda m: m.group(1) + rewrite_target(m.group(2), page, repo, source) + m.group(3), text
    )


def rewrite_markdown(text: str, page: str, repo: dict[str, str], source: Path) -> str:
    out: list[str] = []
    fence: str | None = None
    for line in text.splitlines(keepends=True):
        match = FENCE_RE.match(line)
        if fence:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
            out.append(line)
            continue
        if match:
            fence = match.group(1)
            out.append(line)
            continue
        body = line.rstrip("\r\n")
        out.append(_rewrite_line(body, page, repo, source) + line[len(body):])
    return "".join(out)


def copy_docs(repo: dict[str, str], source: Path, target: Path) -> None:
    docs = source / "docs"
    if not docs.is_dir():
        raise AggregateError(f"{repo['name']}: no docs/ directory at {repo['sha']}.")
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(docs, target)
    for page in target.rglob("*.md"):
        rel = page.relative_to(target).as_posix()
        text = page.read_text(encoding="utf-8")
        page.write_text(rewrite_markdown(text, rel, repo, source), encoding="utf-8", newline="\n")


def prefix_nav(nav: Any, prefix: str) -> Any:
    if isinstance(nav, str):
        return nav if SCHEME_RE.match(nav) else f"{prefix}/{nav}"
    if isinstance(nav, list):
        return [prefix_nav(item, prefix) for item in nav]
    if isinstance(nav, dict):
        return {title: prefix_nav(value, prefix) for title, value in nav.items()}
    raise AggregateError(f"Unsupported nav entry: {nav!r}")


def repo_nav(repo: dict[str, str], source: Path) -> list[Any]:
    config = source / "mkdocs.yml"
    nav = (load_yaml(config) or {}).get("nav") if config.is_file() else None
    if not nav:
        nav = ["index.md"]
    return prefix_nav(nav, f"repos/{repo['name']}")


def generate_config(base: Path, sections: list[dict[str, Any]], output: Path) -> None:
    nav = list((load_yaml(base) or {}).get("nav") or [])
    nav = [item for item in nav if not (isinstance(item, dict) and NAV_SECTION in item)]
    if sections:
        nav.append({NAV_SECTION: sections})
    header = "# Generated by tools/aggregate.py. Do not edit.\n"
    body = yaml.safe_dump({"INHERIT": base.name, "nav": nav}, sort_keys=False, allow_unicode=True)
    output.write_text(header + body, encoding="utf-8", newline="\n")


def parse_local(values: list[str]) -> dict[str, Path]:
    local: dict[str, Path] = {}
    for value in values:
        name, sep, path = value.partition("=")
        if not sep or not name or not path:
            raise AggregateError(f"--local expects NAME=PATH, got '{value}'.")
        local[name] = Path(path).resolve()
    return local


def run(local: dict[str, Path], offline: bool) -> None:
    repos = load_sources()
    unknown = set(local) - {repo["name"] for repo in repos}
    if unknown:
        raise AggregateError(f"--local names not in {SOURCES.name}: {', '.join(sorted(unknown))}.")
    if TARGET.exists():
        shutil.rmtree(TARGET)
    sections = []
    for repo in repos:
        source = local.get(repo["name"])
        if source is None:
            source = CACHE / repo["name"]
            if not offline:
                fetch(repo, source)
            elif not (source / "docs").is_dir():
                raise AggregateError(f"{repo['name']}: not in cache; run without --offline first.")
        copy_docs(repo, source, TARGET / repo["name"])
        sections.append({repo["title"]: repo_nav(repo, source)})
        print(f"{repo['name']}: {repo['sha'][:12]} -> docs/repos/{repo['name']}")
    generate_config(BASE_CONFIG, sections, GENERATED_CONFIG)
    print(f"wrote {GENERATED_CONFIG.name}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", action="append", default=[], metavar="NAME=PATH",
                        help="use a local checkout instead of the pinned SHA")
    parser.add_argument("--offline", action="store_true", help="use cached checkouts only")
    args = parser.parse_args(argv)
    try:
        run(parse_local(args.local), args.offline)
    except (AggregateError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
