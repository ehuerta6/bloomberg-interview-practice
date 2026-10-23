"""Catalog behavior checks; run with unittest discovery from scripts/."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import unittest

from generate_manifest import generate_manifest
from site_catalog import render_catalog


ROOT = Path(__file__).resolve().parents[1]


class CatalogHTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids, self.sections, self.tags = [], [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs["href"])
        if "data-category" in attrs:
            self.sections.append(attrs["data-category"])


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.manifest = generate_manifest(ROOT)
        self.result = render_catalog(self.manifest)
        self.html = CatalogHTML(self.result)

    def test_every_manifest_problem_has_one_existing_page_link(self):
        links = [link for link in self.html.links if link.startswith("problems/")]
        expected = [f'problems/{problem["slug"]}.html' for problem in self.manifest["problems"]]
        self.assertEqual(links, expected)
        self.assertEqual(len(set(links)), 65)
        for link in links:
            self.assertTrue((ROOT / "docs" / link).is_file(), link)

    def test_categories_counts_and_all_difficulties_are_visible(self):
        self.assertEqual(self.html.sections, ["round-1", "round-2", "system-design"])
        self.assertEqual(Counter(p["category"] for p in self.manifest["problems"]), {"round-1": 25, "round-2": 25, "system-design": 15})
        self.assertEqual(self.result.count("25 problems"), 2)
        self.assertIn("15 problems", self.result)
        for difficulty, count in Counter(p["difficulty"] for p in self.manifest["problems"]).items():
            self.assertEqual(self.result.count(f'<span class="tag">{difficulty}</span>'), count)

    def test_navigation_and_skip_targets_exist_without_scripts(self):
        fragments = [link[1:] for link in self.html.links if link.startswith("#")]
        self.assertTrue(all(fragment in self.html.ids for fragment in fragments))
        self.assertEqual(len(self.html.ids), len(set(self.html.ids)))
        self.assertNotIn("script", self.html.tags)
        self.assertIn('href="assets/site.css"', self.result)
        self.assertIn('src="assets/cic-logo.png"', self.result)

    def test_catalog_uses_manifest_metadata_and_escapes_markup(self):
        manifest = {"problems": [dict(self.manifest["problems"][0], title='<img src=x onerror="alert(1)">', difficulty="A & B")]}
        result = render_catalog(manifest)
        self.assertIn('&lt;img src=x onerror=&quot;alert(1)&quot;&gt;', result)
        self.assertIn("A &amp; B", result)
        self.assertIn("1 problems", result)
        self.assertEqual(CatalogHTML(result).tags.count("img"), 1)  # Only the shared logo.
        self.assertEqual(result, render_catalog(manifest))


if __name__ == "__main__":
    unittest.main()
