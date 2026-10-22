"""Runner regression checks: python3 -B scripts/verify-exercises-test.py."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("verify-exercises.py")


class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("verify_exercises", SCRIPT)
        cls.runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.runner)

    def run_fixture(self, source, *, starter=False, expected_errors=(), timeout=5):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / "exercise.py").write_text(source)
            result = self.runner.run_suite(
                directory, "*.py", starter=starter,
                expected_errors=expected_errors, timeout=timeout,
            )
            self.assertFalse(list(directory.glob("__pycache__")))
            return result

    def test_solution_must_run_tests_and_pass(self):
        passing = "import unittest\nclass T(unittest.TestCase):\n def test_ok(self): self.assertEqual(2 + 2, 4)\n"
        self.assertTrue(self.run_fixture(passing)[0])
        self.assertFalse(self.run_fixture(passing.replace("2 + 2, 4", "2 + 2, 5"))[0])
        self.assertFalse(self.run_fixture("import unittest\n")[0])

    def test_starter_requires_an_observed_defect(self):
        failing = "import unittest\nclass T(unittest.TestCase):\n def test_bug(self): self.fail('intentional')\n"
        self.assertTrue(self.run_fixture(failing, starter=True)[0])
        self.assertFalse(self.run_fixture(failing.replace("self.fail('intentional')", "pass"), starter=True)[0])

    def test_import_error_and_process_crash_are_not_expected_failures(self):
        for source in ("import missing_exercise_dependency\n", "raise SystemExit(1)\n", "this is not valid python!\n"):
            with self.subTest(source=source):
                self.assertFalse(self.run_fixture(source, starter=True)[0])

    def test_new_runtime_error_is_rejected_even_with_assertion_failures(self):
        source = "import unittest\nclass T(unittest.TestCase):\n def test_bug(self): self.fail()\n def test_crash(self): raise RuntimeError('new regression')\n"
        self.assertFalse(self.run_fixture(source, starter=True)[0])

    def test_known_error_is_allowed_only_for_matching_test_and_exception(self):
        source = "import unittest\nclass T(unittest.TestCase):\n def test_bug(self): raise TypeError('known defect')\n"
        allowed = (("exercise.T.test_bug", "TypeError"),)
        self.assertTrue(self.run_fixture(source, starter=True, expected_errors=allowed)[0])
        self.assertFalse(self.run_fixture(source.replace("TypeError", "RuntimeError"), starter=True, expected_errors=allowed)[0])
        self.assertFalse(self.run_fixture(source.replace("test_bug", "test_other"), starter=True, expected_errors=allowed)[0])
        self.assertFalse(self.run_fixture(source, expected_errors=allowed)[0])

    def test_subtest_errors_are_checked(self):
        source = "import unittest\nclass T(unittest.TestCase):\n def test_bug(self):\n  with self.subTest(value=1): raise TypeError('known defect')\n"
        allowed = (("exercise.T.test_bug (value=1)", "TypeError"),)
        self.assertTrue(self.run_fixture(source, starter=True, expected_errors=allowed)[0])
        self.assertFalse(self.run_fixture(source, starter=True)[0])

    def test_skips_and_expected_failures_cannot_hide_tests(self):
        for decorator in ("unittest.skip('disabled')", "unittest.expectedFailure"):
            source = f"import unittest\nclass T(unittest.TestCase):\n @{decorator}\n def test_bug(self): self.fail()\n"
            self.assertFalse(self.run_fixture(source, starter=True)[0])
            self.assertFalse(self.run_fixture(source)[0])

    def test_hanging_suite_fails_with_a_timeout(self):
        ok, detail, output = self.run_fixture("while True: pass\n", starter=True, timeout=0.1)
        self.assertFalse(ok)
        self.assertIn("timeout", detail.lower())

    def test_cli_runs_every_pair_and_returns_nonzero_for_regressions(self):
        passing = "import unittest\nclass T(unittest.TestCase):\n def test_ok(self): pass\n"
        failing = passing.replace("pass\n", "self.fail('intentional')\n")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            script = root / "scripts" / SCRIPT.name
            script.parent.mkdir()
            shutil.copyfile(SCRIPT, script)
            for round_name in ("round-1", "round-2"):
                for number in range(1, 26):
                    for base, source in ((root, failing), (root / "solutions", passing)):
                        directory = base / round_name / f"{number:02}-fixture"
                        directory.mkdir(parents=True)
                        (directory / "test_fixture.py").write_text(source)
            command = [sys.executable, "-B", str(script)]
            good = subprocess.run(command, cwd=script.parent, capture_output=True, text=True, timeout=30)
            self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
            self.assertEqual(good.stdout.count("PASS "), 100)
            (root / "solutions/round-1/01-fixture/test_fixture.py").write_text(failing)
            (root / "round-1/02-fixture/test_fixture.py").write_text(passing)
            (root / "round-1/03-fixture/test_fixture.py").write_text("import missing_exercise_dependency\n")
            bad = subprocess.run(command, cwd=script.parent, capture_output=True, text=True, timeout=30)
            self.assertEqual(bad.returncode, 1)
            self.assertEqual(bad.stdout.count("PASS ") + bad.stdout.count("FAIL "), 100)
            for label in ("solution round-1/01-fixture", "starter round-1/02-fixture", "starter round-1/03-fixture"):
                self.assertIn("FAIL " + label, bad.stdout)
            self.assertIn("PASS starter round-2/25-fixture", bad.stdout)
            self.assertIn("ModuleNotFoundError", bad.stderr)

    def test_inventory_requires_25_matching_exercises_per_round(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for round_name in ("round-1", "round-2"):
                for number in range(1, 26):
                    for base in (root, root / "solutions"):
                        (base / round_name / f"{number:02}-fixture").mkdir(parents=True)
            self.assertEqual(len(self.runner.discover_exercises(root)), 50)
            (root / "solutions/round-1/01-fixture").rmdir()
            with self.assertRaises(ValueError):
                self.runner.discover_exercises(root)


if __name__ == "__main__":
    unittest.main()
