import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import aggregate  # noqa: E402

SHA = "0123456789abcdef0123456789abcdef01234567"
REPO = {"name": "demo", "title": "Demo", "url": "https://github.com/sogeor/demo", "ref": "master", "sha": SHA}
BLOB = f"https://github.com/sogeor/demo/blob/{SHA}"
TREE = f"https://github.com/sogeor/demo/tree/{SHA}"


class RewriteTargetTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.source = Path(self.tmp.name)
        (self.source / "docs" / "adr").mkdir(parents=True)
        (self.source / "tests").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def rewrite(self, target, page="index.md"):
        return aggregate.rewrite_target(target, page, REPO, self.source)

    def test_keeps_links_inside_docs(self):
        self.assertEqual(self.rewrite("setup.md#tokens"), "setup.md#tokens")
        self.assertEqual(self.rewrite("../index.md", "adr/0001.md"), "../index.md")

    def test_keeps_external_anchor_and_absolute(self):
        for target in ("https://example.com", "mailto:a@example.com", "#top", "/abs"):
            self.assertEqual(self.rewrite(target), target)

    def test_rewrites_file_outside_docs(self):
        self.assertEqual(self.rewrite("../README.md#versions"), f"{BLOB}/README.md#versions")
        self.assertEqual(self.rewrite("../../LICENSE", "adr/0001.md"), f"{BLOB}/LICENSE")

    def test_rewrites_directory_and_root(self):
        self.assertEqual(self.rewrite("../tests"), f"{TREE}/tests")
        self.assertEqual(self.rewrite(".."), TREE)

    def test_angle_brackets_preserved(self):
        self.assertEqual(self.rewrite("<../README.md>"), f"<{BLOB}/README.md>")

    def test_rejects_links_outside_repository(self):
        with self.assertRaises(aggregate.AggregateError):
            self.rewrite("../../other/README.md")


class RewriteMarkdownTest(unittest.TestCase):
    def test_skips_code_and_rewrites_links(self):
        text = (
            "See [readme](../README.md) and [setup](setup.md \"Setup\").\n"
            "Inline `[x](../README.md)` stays.\n"
            "```text\n[x](../README.md)\n```\n"
            "[ref]: ../LICENSE\n"
            "![img](../assets/a.png)\n"
        )
        expected = (
            f"See [readme]({BLOB}/README.md) and [setup](setup.md \"Setup\").\n"
            "Inline `[x](../README.md)` stays.\n"
            "```text\n[x](../README.md)\n```\n"
            f"[ref]: {BLOB}/LICENSE\n"
            f"![img]({BLOB}/assets/a.png)\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(aggregate.rewrite_markdown(text, "index.md", REPO, Path(tmp)), expected)


class NavTest(unittest.TestCase):
    def test_prefix_nav(self):
        nav = ["index.md", {"Ref": [{"A": "reference/a.md"}, {"Ext": "https://example.com"}]}]
        self.assertEqual(
            aggregate.prefix_nav(nav, "repos/demo"),
            ["repos/demo/index.md", {"Ref": [{"A": "repos/demo/reference/a.md"}, {"Ext": "https://example.com"}]}],
        )

    def test_generate_config_replaces_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "mkdocs.yml"
            base.write_text(
                "site_name: x\nmarkdown_extensions:\n  - pymdownx.superfences:\n"
                "      custom_fences:\n        - format: !!python/name:pymdownx.superfences.fence_code_format\n"
                "nav:\n  - Home: index.md\n  - Repositories: []\n",
                encoding="utf-8",
            )
            out = Path(tmp) / "mkdocs.generated.yml"
            aggregate.generate_config(base, [{"Demo": ["repos/demo/index.md"]}], out)
            data = aggregate.load_yaml(out)
        self.assertEqual(data["INHERIT"], "mkdocs.yml")
        self.assertEqual(data["nav"], [{"Home": "index.md"}, {"Repositories": [{"Demo": ["repos/demo/index.md"]}]}])


class SourcesTest(unittest.TestCase):
    def load(self, body):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sources.yaml"
            path.write_text(body, encoding="utf-8")
            return aggregate.load_sources(path)

    def test_valid(self):
        repos = self.load(
            f"repositories:\n  - name: demo\n    title: Demo\n    url: https://github.com/sogeor/demo\n"
            f"    ref: master\n    sha: {SHA}\n"
        )
        self.assertEqual(repos[0]["name"], "demo")

    def test_rejects_short_sha(self):
        with self.assertRaises(aggregate.AggregateError):
            self.load(
                "repositories:\n  - name: demo\n    title: Demo\n    url: https://github.com/sogeor/demo\n"
                "    ref: master\n    sha: 0123abc\n"
            )

    def test_rejects_duplicates(self):
        entry = (
            f"  - name: demo\n    title: Demo\n    url: https://github.com/sogeor/demo\n"
            f"    ref: master\n    sha: {SHA}\n"
        )
        with self.assertRaises(aggregate.AggregateError):
            self.load("repositories:\n" + entry + entry)


if __name__ == "__main__":
    unittest.main()
