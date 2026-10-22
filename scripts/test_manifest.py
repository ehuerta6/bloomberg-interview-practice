"""Run with: python3 -m unittest discover -s scripts -p 'test_manifest.py' -v."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from generate_manifest import ManifestError, generate_manifest, render_manifest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/generate_manifest.py"


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for category, count, prefix in (
            ("round-1", 25, "PR #"),
            ("round-2", 25, "Ticket #"),
            ("system-design", 15, "Problem "),
        ):
            directory = category if category == "system-design" else f"problems/{category}"
            for number in range(1, count + 1):
                stem = f"{number:02d}-example-{number}"
                source = self.root / directory / f"{stem}.md"
                source.parent.mkdir(parents=True, exist_ok=True)
                text = f"# {prefix}{number:02d} — Example {number}\n\n**Difficulty:** Easy\n"
                if category != "system-design":
                    starter = self.root / category / stem
                    starter.mkdir(parents=True)
                    text += f"\n## Starter Code\n\n[View starter code](../../{category}/{stem}/)\n"
                    solution = self.root / "solutions" / category / stem
                    solution.mkdir(parents=True)
                    link = f"../../solutions/{category}/{stem}/"
                else:
                    solution = self.root / "solutions" / category / f"{stem}.md"
                    solution.parent.mkdir(parents=True, exist_ok=True)
                    solution.write_text("# Reference\n", encoding="utf-8")
                    link = f"../solutions/{category}/{stem}.md"
                source.write_text(text + f"\n## Reference Solution\n\n[View solution]({link})\n", encoding="utf-8")
        self.source = self.root / "problems/round-1/01-example-1.md"

    def replace(self, before, after):
        self.source.write_text(self.source.read_text(encoding="utf-8").replace(before, after), encoding="utf-8")

    def test_real_repository_counts_paths_and_artifact(self):
        manifest = generate_manifest(ROOT)
        entries = manifest["problems"]
        self.assertEqual([sum(p["category"] == c for p in entries) for c in ("round-1", "round-2", "system-design")], [25, 25, 15])
        self.assertEqual(len({p["id"] for p in entries}), 65)
        self.assertEqual(len({p["slug"] for p in entries}), 65)
        for entry in entries:
            for field in ("source_path", "starter_path", "solution_path"):
                if entry[field] is not None:
                    self.assertTrue((ROOT / entry[field]).exists())
        self.assertEqual((ROOT / "scripts/problem-manifest.json").read_text(encoding="utf-8"), render_manifest(manifest))

    def test_metadata_and_stable_identity_come_from_sources(self):
        self.replace("Example 1\n", "Café & Review\n")
        self.replace("**Difficulty:** Easy", "**Difficulty:** Hard")
        entry = generate_manifest(self.root)["problems"][0]
        self.assertEqual(entry, {
            "id": "round-1-01", "category": "round-1", "number": 1,
            "slug": "round-1-01-example-1", "title": "Café & Review", "difficulty": "Hard",
            "source_path": "problems/round-1/01-example-1.md",
            "starter_path": "round-1/01-example-1", "solution_path": "solutions/round-1/01-example-1",
        })

    def test_system_design_has_no_starter(self):
        entries = generate_manifest(self.root)["problems"][50:]
        self.assertTrue(all(p["starter_path"] is None for p in entries))
        self.assertEqual(entries[0]["solution_path"], "solutions/system-design/01-example-1.md")

    def test_deterministic_serialization(self):
        first = render_manifest(generate_manifest(self.root))
        self.assertEqual(first, render_manifest(generate_manifest(self.root)))
        with tempfile.TemporaryDirectory() as other:
            copied = Path(other) / "another-checkout"
            shutil.copytree(self.root, copied)
            self.assertEqual(first, render_manifest(generate_manifest(copied)))
        self.assertTrue(first.endswith("\n"))
        self.assertEqual(json.loads(first)["schema_version"], 1)

    def test_missing_source_rejected(self):
        self.source.unlink()
        with self.assertRaisesRegex(ManifestError, "25"):
            generate_manifest(self.root)

    def test_duplicate_number_rejected(self):
        self.source.with_name("02-extra-example.md").write_text(self.source.read_text(encoding="utf-8"), encoding="utf-8")
        self.source.unlink()
        with self.assertRaisesRegex(ManifestError, "duplicate"):
            generate_manifest(self.root)

    def test_noncontiguous_numbers_rejected(self):
        self.source.rename(self.source.with_name("26-example-1.md"))
        with self.assertRaisesRegex(ManifestError, "number"):
            generate_manifest(self.root)

    def test_invalid_filename_rejected(self):
        self.source.rename(self.source.with_name("01_Example.md"))
        with self.assertRaisesRegex(ManifestError, "filename"):
            generate_manifest(self.root)

    def test_wrong_heading_number_rejected(self):
        self.replace("PR #01", "PR #02")
        with self.assertRaisesRegex(ManifestError, "heading"):
            generate_manifest(self.root)

    def test_missing_or_duplicate_difficulty_rejected(self):
        for replacement in ("", "**Difficulty:** Expert", "**Difficulty:** Easy\n**Difficulty:** Hard"):
            with self.subTest(replacement=replacement):
                original = self.source.read_text(encoding="utf-8")
                self.replace("**Difficulty:** Easy", replacement)
                with self.assertRaisesRegex(ManifestError, "difficulty"):
                    generate_manifest(self.root)
                self.source.write_text(original, encoding="utf-8")

    def test_missing_link_rejected(self):
        self.replace("[View starter code]", "View starter code")
        with self.assertRaisesRegex(ManifestError, "Starter Code"):
            generate_manifest(self.root)

    def test_missing_target_rejected(self):
        (self.root / "round-1/01-example-1").rmdir()
        with self.assertRaisesRegex(ManifestError, "missing"):
            generate_manifest(self.root)

    def test_target_type_and_symlink_escape_rejected(self):
        target = self.root / "round-1/01-example-1"
        target.rmdir()
        target.write_text("not a directory", encoding="utf-8")
        with self.assertRaisesRegex(ManifestError, "missing"):
            generate_manifest(self.root)
        target.unlink()
        with tempfile.TemporaryDirectory() as outside:
            target.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ManifestError, "escapes"):
                generate_manifest(self.root)

    def test_wrong_exercise_link_rejected(self):
        self.replace("../../round-1/01-example-1/", "../../round-1/02-example-2/")
        with self.assertRaisesRegex(ManifestError, "expected"):
            generate_manifest(self.root)

    def test_external_and_escaping_links_rejected(self):
        for link in ("https://example.com/starter", "../../../outside", "/tmp", "../../round-1/01-example-1/#fragment"):
            with self.subTest(link=link):
                original = self.source.read_text(encoding="utf-8")
                self.replace("../../round-1/01-example-1/", link)
                with self.assertRaises(ManifestError):
                    generate_manifest(self.root)
                self.source.write_text(original, encoding="utf-8")

    def test_check_mode_detects_missing_stale_and_current_output(self):
        output = self.root / "manifest.json"
        command = [sys.executable, str(SCRIPT), "--root", str(self.root), "--output", str(output)]
        missing = subprocess.run(command + ["--check"], capture_output=True, text=True)
        self.assertEqual(missing.returncode, 1)
        self.assertIn("missing", missing.stderr)
        generated = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(generated.returncode, 0, generated.stderr)
        original = output.read_bytes()
        current = subprocess.run(command + ["--check"], capture_output=True, text=True)
        self.assertEqual(current.returncode, 0, current.stderr)
        self.replace("Example 1\n", "Revised title\n")
        stale = subprocess.run(command + ["--check"], capture_output=True, text=True)
        self.assertEqual(stale.returncode, 1)
        self.assertIn("stale", stale.stderr)
        self.assertEqual(output.read_bytes(), original)
        self.replace("**Difficulty:** Easy", "**Difficulty:** Unknown")
        invalid = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(invalid.returncode, 1)
        self.assertIn("difficulty", invalid.stderr)
        self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
