"""Focused renderer/build checks; run with unittest discovery from scripts/."""

from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from site_renderer import REPOSITORY_URL, SITE_FILES, render_markdown, render_page


SPEC = importlib.util.spec_from_file_location("build_site", Path(__file__).with_name("build-site.py"))
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)
ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("problems/round-1/01-code-validator.md")


class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def attributes(self, tag, attr):
        return [attrs[attr] for name, attrs in self.elements if name == tag and attr in attrs]


class RendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = build.generate_manifest(ROOT)
        cls.pages = {p["source_path"]: p["slug"] for p in cls.manifest["problems"]}

    def render(self, markdown):
        return render_markdown(markdown, SOURCE, ROOT, self.pages)

    def test_markdown_fixture_formats_tables_lists_code_and_quotes(self):
        result = self.render((SITE_FILES / "fixtures/renderer.md").read_text())
        tags = [tag for tag, _ in HTML(result).elements]
        for tag in ("h1", "strong", "em", "s", "code", "ul", "blockquote", "table", "th", "td"):
            self.assertIn(tag, tags)
        self.assertIn('class="table-scroll"', result)
        self.assertIn('class="language-python"', result)
        self.assertIn("value &lt; 10", result)

    def test_raw_markup_and_code_are_escaped(self):
        result = self.render('<script>alert(1)</script>\n\n<img src=x onerror=alert(1)>\n\n```html\n</code><script>alert(1)</script>\n```')
        self.assertNotIn("script", [tag for tag, _ in HTML(result).elements])
        self.assertNotIn("img", [tag for tag, _ in HTML(result).elements])
        self.assertIn("&lt;script&gt;", result)
        self.assertIn("&lt;/code&gt;", result)

    def test_unsafe_link_schemes_are_never_active(self):
        for url in ("javascript:alert%281%29", "JaVaScRiPt:alert%281%29", "vbscript:msgbox%281%29", "data:text/html,payload", "data:image/png;base64,AAAA", "file:///etc/passwd", "//example.com", "custom:payload"):
            with self.subTest(url=url):
                self.assertEqual(HTML(self.render(f"[x]({url})")).attributes("a", "href"), [])

    def test_url_attribute_quotes_cannot_escape(self):
        result = self.render('[x](https://example.com/?q=%22%20onclick=%22alert%281%29 "a & b")')
        attrs = [attrs for tag, attrs in HTML(result).elements if tag == "a"][0]
        self.assertEqual(set(attrs), {"href", "title"})
        self.assertEqual(attrs["title"], "a & b")

    def test_relative_starter_solution_and_cross_problem_links(self):
        result = self.render('[start](../../round-1/01-code-validator/)\n[solution](../../solutions/round-1/01-code-validator/)\n[next](02-event-scheduler.md#expected-behavior)')
        self.assertEqual(HTML(result).attributes("a", "href"), [
            REPOSITORY_URL + "/tree/main/round-1/01-code-validator",
            REPOSITORY_URL + "/tree/main/solutions/round-1/01-code-validator",
            "round-1-02-event-scheduler.html#heading-expected-behavior",
        ])

    def test_system_design_reference_stays_an_explicit_github_link(self):
        result = render_page(self.manifest["problems"][50], ROOT, self.pages)
        self.assertIn(REPOSITORY_URL + "/blob/main/solutions/system-design/01-gym-class-signup.md", result)
        self.assertNotIn("```mermaid", result)

    def test_external_url_query_and_fragment_are_preserved(self):
        result = self.render('[x](https://example.com/?a=1&b=2#part) [mail](mailto:hello@example.com)')
        self.assertEqual(HTML(result).attributes("a", "href"), ["https://example.com/?a=1&b=2#part", "mailto:hello@example.com"])

    def test_anchors_are_prefixed_unique_and_linked(self):
        result = self.render("## Location\n\n## Location\n\n## Location-1\n\n[go](#location) [duplicate](#location-1)")
        ids = HTML(result).attributes("h2", "id")
        self.assertEqual(ids, ["heading-location", "heading-location-1", "heading-location-1-1"])
        self.assertEqual(HTML(result).attributes("a", "href"), ["#heading-location", "#heading-location-1"])

    def test_local_images_use_repository_raw_url(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "picture.png").write_bytes(b"image")
            result = render_markdown("![Picture](picture.png)", Path("problem.md"), root, {})
            self.assertEqual(HTML(result).attributes("img", "src"), [REPOSITORY_URL + "/raw/main/picture.png"])

    def test_missing_or_escaping_local_links_fail(self):
        for url in ("../../../outside.md", "%2e%2e/%2e%2e/%2e%2e/outside.md", "missing.md", "/etc/passwd", r"..%5coutside.md"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                self.render(f"[x]({url})")

    def test_mermaid_source_is_escaped_before_browser_rendering(self):
        result = self.render('```mermaid\nflowchart LR\nA["</pre><script>alert(1)</script>"]\n```')
        self.assertEqual(HTML(result).attributes("pre", "class"), ["mermaid"])
        self.assertNotIn("script", [tag for tag, _ in HTML(result).elements])
        self.assertIn("&lt;/pre&gt;&lt;script&gt;", result)

    def test_page_metadata_is_escaped(self):
        problem = dict(self.manifest["problems"][0], title='</title><script>alert(1)</script>')
        result = render_page(problem, ROOT, self.pages)
        self.assertIn("&lt;/title&gt;&lt;script&gt;", result)
        self.assertEqual(HTML(result).attributes("script", "src"), [])

    def test_mermaid_module_is_emitted_only_for_mermaid_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            problem = dict(self.manifest["problems"][0], source_path="fixture.md")
            source = root / "fixture.md"
            for markdown, scripts in (
                ("# Ordinary page\n\n```python\nprint('hi')\n```", []),
                ('# Plain code\n\n```html\n<pre class="mermaid">\n```', []),
                ("# Diagram page\n\n```mermaid\nflowchart LR\nA --> B\n```", ["../renderer/mermaid.mjs"]),
            ):
                with self.subTest(markdown=markdown):
                    source.write_text(markdown)
                    self.assertEqual(HTML(render_page(problem, root, {})).attributes("script", "src"), scripts)


class BuildTests(unittest.TestCase):
    def snapshot(self, directory):
        return {path.relative_to(directory).as_posix(): path.read_bytes() for path in directory.rglob("*") if path.is_file()}

    def test_65_pages_and_module_build_identically_in_clean_directories(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first, second = Path(first), Path(second)
            build.build_site(ROOT, first)
            build.build_site(ROOT, second)
            before = self.snapshot(first)
            self.assertEqual(before, self.snapshot(second))
            self.assertEqual(len(list((first / "problems").glob("*.html"))), 65)
            for page in (first / "problems").glob("*.html"):
                self.assertEqual(HTML(page.read_text()).attributes("script", "src"), [])
            for prefix, count in (("round-1", 25), ("round-2", 25), ("system-design", 15)):
                self.assertEqual(len(list((first / "problems").glob(prefix + "-*.html"))), count)
            build.build_site(ROOT, first, check=True)
            build.build_site(ROOT, first)
            self.assertEqual(before, self.snapshot(first))

    def test_check_detects_missing_and_stale_output_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with self.assertRaisesRegex(ValueError, "missing or stale"):
                build.build_site(ROOT, output, check=True)
            self.assertEqual(self.snapshot(output), {})
            build.build_site(ROOT, output)
            page = next((output / "problems").glob("*.html"))
            page.write_text("stale")
            before = self.snapshot(output)
            with self.assertRaisesRegex(ValueError, "missing or stale"):
                build.build_site(ROOT, output, check=True)
            self.assertEqual(before, self.snapshot(output))

    def test_stale_owned_pages_removed_and_other_site_files_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            build.build_site(ROOT, output)
            stale = output / "problems/old-problem.html"
            stale.write_bytes(build.GENERATED_MARKER + b"\nold")
            (output / "index.html").write_text("owned by catalog")
            with self.assertRaisesRegex(ValueError, "missing or stale"):
                build.build_site(ROOT, output, check=True)
            build.build_site(ROOT, output)
            self.assertFalse(stale.exists())
            self.assertEqual((output / "index.html").read_text(), "owned by catalog")

    def test_unowned_pages_are_never_deleted(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output / "problems").mkdir()
            page = output / "problems/manual.html"
            page.write_text("keep")
            with self.assertRaisesRegex(ValueError, "unowned"):
                build.build_site(ROOT, output)
            self.assertEqual(page.read_text(), "keep")

    def test_stale_manifest_fails_before_output_is_written(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with patch.object(build, "render_manifest", return_value="stale"):
                with self.assertRaisesRegex(ValueError, "manifest is stale"):
                    build.build_site(ROOT, output)
            self.assertEqual(self.snapshot(output), {})


if __name__ == "__main__":
    unittest.main()
