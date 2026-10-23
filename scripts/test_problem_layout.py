"""Shared detail layout and deliberate reference-link disclosure checks."""

from html.parser import HTMLParser
from pathlib import Path
import unittest
from unittest.mock import patch

from generate_manifest import generate_manifest
from site_renderer import render_markdown, render_page, repository_link


ROOT = Path(__file__).resolve().parents[1]
OPENING = '<details class="solution-reveal">\n<summary>Reveal reference solution link</summary>\n<div class="details-content">\n'
CLOSING = '</div>\n</details>\n'


class PageHTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.references, self.disclosures = [], [], []
        self.in_reference = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "details" and attrs.get("class") == "solution-reveal":
            self.disclosures.append(attrs)
            self.in_reference = True
        elif tag == "a":
            self.links.append(attrs["href"])
            if "/solutions/" in attrs["href"]:
                self.references.append((attrs["href"], self.in_reference))

    def handle_endtag(self, tag):
        if tag == "details":
            self.in_reference = False


class ProblemLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = generate_manifest(ROOT)
        cls.pages = {p["source_path"]: p["slug"] for p in cls.manifest["problems"]}

    def test_all_65_pages_have_closed_disclosure_correct_links_and_shared_layout(self):
        for problem in self.manifest["problems"]:
            with self.subTest(problem=problem["id"]):
                result = render_page(problem, ROOT, self.pages)
                html = PageHTML(result)
                self.assertEqual(html.disclosures, [{"class": "solution-reveal"}])
                solution = repository_link(problem["solution_path"], directory=problem["category"] != "system-design")
                self.assertEqual(html.references, [(solution, True)])
                self.assertIn(repository_link(problem["source_path"]), html.links)
                if problem["starter_path"]:
                    self.assertIn(repository_link(problem["starter_path"], directory=True), html.links)
                self.assertIn(f'../index.html#{problem["category"]}', html.links)
                self.assertIn('class="breadcrumbs"', result)
                self.assertIn('class="prose"', result)
                self.assertNotIn("<iframe", result)

    def test_disclosure_preserves_every_assignment_token_and_link(self):
        for problem in self.manifest["problems"]:
            with self.subTest(problem=problem["id"]):
                source = Path(problem["source_path"])
                markdown = (ROOT / source).read_text(encoding="utf-8")
                ordinary = render_markdown(markdown, source, ROOT, self.pages)
                disclosed = render_markdown(markdown, source, ROOT, self.pages, reveal_solutions=True)
                self.assertEqual(disclosed.replace(OPENING, "").replace(CLOSING, ""), ordinary)

    def test_generation_never_reads_reference_solution_contents(self):
        read_text = Path.read_text

        def reject_solution_read(path, *args, **kwargs):
            if (ROOT / "solutions") in path.parents:
                self.fail(f"attempted solution read: {path}")
            return read_text(path, *args, **kwargs)

        with patch.object(Path, "read_text", reject_solution_read):
            for problem in self.manifest["problems"]:
                render_page(problem, ROOT, self.pages)

    def test_disclosure_ends_at_next_section_and_ignores_fenced_heading(self):
        markdown = "# Example\n\n```md\n## Reference Solution\n```\n\n## Reference Solution\n\n[Compare](https://example.com/reference)\n\n## Next task\n\nKeep this visible."
        result = render_markdown(markdown, Path("fixture.md"), ROOT, {}, reveal_solutions=True)
        self.assertEqual(result.count(OPENING), 1)
        self.assertIn('</details>\n<h2 id="heading-next-task">Next task</h2>', result)
        self.assertEqual(result.replace(OPENING, "").replace(CLOSING, ""), render_markdown(markdown, Path("fixture.md"), ROOT, {}))


if __name__ == "__main__":
    unittest.main()
