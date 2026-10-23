#!/usr/bin/env python3
"""Run exporter checks: python3 scripts/export-exercise-tests.py."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile


SCRIPT = Path(__file__).with_name("export-exercise.py")


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.write("AGENTS.md", "Shared practice policy\n")
        self.write("round-1/01-example/AGENTS.md", "Local round 1 policy\n")
        self.write("round-1/01-example/starter.py", "assert 1 + 1 == 2\n")
        self.write("round-2/01-example/AGENTS.md", "Local round 2 policy\n")
        self.write("round-2/01-example/models.py", "VALUE = 3\n")
        self.write("round-2/01-example/test_example.py", "from models import VALUE\nassert VALUE == 3\n")
        for path in (
            "round-1/02-unrelated/unrelated.py",
            "solutions/round-1/01-example/starter.py",
            "problems/round-1/01-example.md",
            "round-1/01-example/README.md",
            "round-1/01-example/solutions/answer.py",
        ):
            self.write(path, "DO NOT EXPORT\n")
        self.manifest = {
            "schema_version": 1,
            "problems": [
                {"id": "round-1-01", "category": "round-1", "starter_path": "round-1/01-example"},
                {"id": "round-2-01", "category": "round-2", "starter_path": "round-2/01-example"},
                {"id": "system-design-01", "category": "system-design", "starter_path": None},
            ],
        }
        self.save_manifest()
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        self.write("round-1/01-example/scratch.py", "DO NOT EXPORT\n")

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def save_manifest(self):
        self.write("scripts/problem-manifest.json", json.dumps(self.manifest))

    def export(self, problem="round-1-01", output=None):
        output = output or self.root / "package.zip"
        result = subprocess.run(
            [sys.executable, str(SCRIPT), problem, "--root", str(self.root), "--output", str(output)],
            capture_output=True, text=True,
        )
        return result, output

    def assert_export_error(self, result, output):
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Export error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(output.exists())

    def test_round_1_has_only_starter_and_policies(self):
        result, output = self.export()
        self.assertEqual(result.returncode, 0, result.stderr)
        with ZipFile(output) as package:
            self.assertEqual(package.namelist(), [
                "AGENTS.md", "round-1/01-example/AGENTS.md", "round-1/01-example/starter.py",
            ])
            self.assertEqual(package.read("round-1/01-example/starter.py"), b"assert 1 + 1 == 2\n")
            package.extractall(self.root / "extracted")
        run = subprocess.run([sys.executable, "starter.py"], cwd=self.root / "extracted/round-1/01-example")
        self.assertEqual(run.returncode, 0)

    def test_round_2_tests_run_with_local_imports(self):
        result, output = self.export("round-2-01")
        self.assertEqual(result.returncode, 0, result.stderr)
        with ZipFile(output) as package:
            self.assertEqual(package.namelist(), [
                "AGENTS.md", "round-2/01-example/AGENTS.md",
                "round-2/01-example/models.py", "round-2/01-example/test_example.py",
            ])
            package.extractall(self.root / "extracted")
        run = subprocess.run([sys.executable, "test_example.py"], cwd=self.root / "extracted/round-2/01-example")
        self.assertEqual(run.returncode, 0)

    def test_archive_is_identical_after_source_mtime_and_mode_changes(self):
        result, first = self.export(output=self.root / "first.zip")
        self.assertEqual(result.returncode, 0, result.stderr)
        starter = self.root / "round-1/01-example/starter.py"
        starter.touch()
        starter.chmod(0o755)
        result, second = self.export(output=self.root / "second.zip")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_rejects_unknown_and_non_coding_ids(self):
        for problem in ("round-1-99", "system-design-01", "../solutions"):
            with self.subTest(problem=problem):
                result, output = self.export(problem)
                self.assert_export_error(result, output)

    def test_rejects_manifest_escape_or_wrong_exercise(self):
        for path in ("../outside", "solutions/round-1/01-example", "round-2/01-example", "round-1/02-unrelated"):
            with self.subTest(path=path):
                self.manifest["problems"][0]["starter_path"] = path
                self.save_manifest()
                result, output = self.export()
                self.assert_export_error(result, output)

    def test_rejects_symlink_file(self):
        starter = self.root / "round-1/01-example/starter.py"
        starter.unlink()
        starter.symlink_to(self.root / "solutions/round-1/01-example/starter.py")
        result, output = self.export()
        self.assert_export_error(result, output)

    def test_rejects_symlink_directory(self):
        folder = self.root / "round-1/01-example"
        folder.rename(self.root / "elsewhere")
        folder.symlink_to(self.root / "elsewhere", target_is_directory=True)
        result, output = self.export()
        self.assert_export_error(result, output)

    def test_does_not_overwrite_existing_output(self):
        self.write("package.zip", "KEEP\n")
        result, output = self.export()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Export error:", result.stderr)
        self.assertEqual(output.read_bytes(), b"KEEP\n")

    def test_missing_tracked_starter_fails_without_output(self):
        (self.root / "round-1/01-example/starter.py").unlink()
        result, output = self.export()
        self.assert_export_error(result, output)

    def test_missing_shared_policy_fails_without_output(self):
        (self.root / "AGENTS.md").unlink()
        result, output = self.export()
        self.assert_export_error(result, output)

    def test_missing_tracked_local_policy_fails_without_output(self):
        (self.root / "round-1/01-example/AGENTS.md").unlink()
        result, output = self.export()
        self.assert_export_error(result, output)

    def test_rejects_unknown_manifest_version(self):
        self.manifest["schema_version"] = 2
        self.save_manifest()
        result, output = self.export()
        self.assert_export_error(result, output)

    def test_rejects_ambiguous_selection(self):
        self.manifest["problems"].append(dict(self.manifest["problems"][0]))
        self.save_manifest()
        result, output = self.export()
        self.assert_export_error(result, output)

    def test_default_output_uses_ignored_context_directory(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "round-1-01", "--root", str(self.root)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / ".local-context/exports/round-1-01.zip").is_file())


if __name__ == "__main__":
    unittest.main()
