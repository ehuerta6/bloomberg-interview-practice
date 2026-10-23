"""Synthetic CI fixtures prove missing links/assets and paths fail closed."""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from verify_site import REPOSITORY, validate_site


class SiteValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="cic-ci-fixture-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.site = self.root / "docs"
        self.write("docs/assets/site.css", "body { color: #111; }")
        self.write("docs/assets/cic-logo.png", "synthetic image asset")
        problems = []
        links = []
        for category, count in (("round-1", 25), ("round-2", 25), ("system-design", 15)):
            for number in range(1, count + 1):
                slug = f"{category}-{number:02d}-fixture"
                source = f"problems/{slug}.md"
                solution = f"solutions/{slug}" + (".md" if category == "system-design" else "")
                starter = None if category == "system-design" else f"{category}/{number:02d}-fixture"
                self.write(source, "# Synthetic source")
                if category == "system-design":
                    self.write(solution, "Synthetic reference target")
                else:
                    (self.root / solution).mkdir(parents=True)
                    (self.root / starter).mkdir(parents=True)
                problem = dict(id=f"{category}-{number:02d}", category=category, slug=slug,
                               source_path=source, starter_path=starter, solution_path=solution)
                problems.append(problem)
                resource = REPOSITORY + ("/blob/main/" if category == "system-design" else "/tree/main/") + solution
                body = f'<a href="{REPOSITORY}/blob/main/{source}">Source</a><a href="{resource}">Reference</a>'
                if starter:
                    body += f'<a href="{REPOSITORY}/tree/main/{starter}">Starter</a>'
                self.write(f"docs/problems/{slug}.html",
                           '<link href="../assets/site.css"><img src="../assets/cic-logo.png">'
                           f'<a href="../index.html#catalog">Catalog</a><article data-problem-id="{problem["id"]}" id="assignment">{body}</article>')
                links.append(f'<a href="problems/{slug}.html">Problem</a>')
        self.write("scripts/problem-manifest.json", json.dumps({"problems": problems}))
        self.write("docs/index.html", '<main id="catalog">' + "".join(links) + "</main>")
        self.page = self.site / "problems/round-1-01-fixture.html"

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def validate(self):
        with redirect_stdout(StringIO()):
            validate_site(self.root)

    def append(self, markup):
        self.page.write_text(self.page.read_text() + markup, encoding="utf-8")

    def test_complete_65_page_fixture_passes(self):
        self.validate()

    def test_missing_problem_page_fails(self):
        self.page.unlink()
        with self.assertRaisesRegex(ValueError, "exactly match all 65"):
            self.validate()

    def test_catalog_omission_fails(self):
        catalog = self.site / "index.html"
        catalog.write_text(catalog.read_text().replace('<a href="problems/round-1-01-fixture.html">Problem</a>', ""))
        with self.assertRaisesRegex(ValueError, "exactly once"):
            self.validate()

    def test_missing_local_link_and_encoded_fragment_fail(self):
        for reference, message in (("missing.html", "missing local target"),
                                   ("../index.html#no%2Dsuch%2Did", "missing fragment")):
            with self.subTest(reference=reference):
                original = self.page.read_text()
                self.append(f'<a href="{reference}">Broken</a>')
                with self.assertRaisesRegex(ValueError, message):
                    self.validate()
                self.page.write_text(original)

    def test_missing_asset_fails(self):
        (self.site / "assets/cic-logo.png").unlink()
        with self.assertRaisesRegex(ValueError, "missing local target"):
            self.validate()

    def test_missing_repository_source_target_fails(self):
        (self.root / "problems/round-1-01-fixture.md").unlink()
        with self.assertRaisesRegex(ValueError, "missing repository target"):
            self.validate()

    def test_wrong_resource_link_fails(self):
        self.page.write_text(self.page.read_text().replace("/tree/main/round-1/01-fixture", "/tree/main/round-1/02-fixture"))
        with self.assertRaisesRegex(ValueError, "manifest resource link"):
            self.validate()

    def test_unsafe_paths_and_schemes_fail(self):
        for reference in ("/index.html", "../../AGENTS.md", "..%5Cescape.html", "//elsewhere.invalid", "javascript:alert(1)"):
            with self.subTest(reference=reference):
                original = self.page.read_text()
                self.append(f'<a href="{reference}">Invalid</a>')
                with self.assertRaises(ValueError):
                    self.validate()
                self.page.write_text(original)

    def test_duplicate_fragment_target_fails(self):
        self.append('<div id="assignment">Duplicate</div>')
        with self.assertRaisesRegex(ValueError, "duplicate HTML ids"):
            self.validate()

    def test_missing_css_asset_fails(self):
        self.write("docs/assets/site.css", 'body { background: url("missing.png"); }')
        with self.assertRaisesRegex(ValueError, "missing local target"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
