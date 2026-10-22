#!/usr/bin/env python3
"""Check all 50 Python exercises with the standard library only.

Run from any directory: python3 /path/to/repo/scripts/verify-exercises.py
Solutions must pass; starters must expose a defect without new runtime errors.
Known starter exception-type defects are listed below. Each suite runs in its
own Python process with a 10-second timeout and bytecode writes disabled.
Runner regression checks: python3 -B scripts/verify-exercises-test.py
"""

import argparse
import json
from pathlib import Path
import subprocess
import sys


# These existing teaching defects raise the wrong exception instead of failing
# an assertion. All other runtime/import errors are regressions, even if other
# tests in the same starter still have assertion failures.
EXPECTED_STARTER_ERRORS = {
    "round-1/09-gradebook-aggregation": (
        ("gradebook.GradebookTests.test_invalid_weights_and_category_names_are_rejected (weights=[])", "ZeroDivisionError"),
    ),
    "round-1/10-csv-import-parser": (
        ("csv_import.CsvImportTests.test_header_whitespace_is_ignored", "ValueError"),
        ("csv_import.CsvImportTests.test_quoted_comma_in_email_display_value_is_preserved", "ValueError"),
    ),
    "round-1/15-balance-transfer": (
        ("transfers.BalanceTransferTests.test_unhashable_account_id_is_rejected", "TypeError"),
    ),
    "round-1/16-log-filtering": (
        ("log_filter.LogFilterTests.test_malformed_entries_are_skipped", "KeyError"),
    ),
    "round-1/18-dependency-resolution": (
        ("dependency_resolver.DependencyResolverTests.test_invalid_graph_shape_is_rejected", "TypeError"),
    ),
    "round-1/23-reservation-expiration": (
        ("reservations.ReservationTests.test_naive_and_aware_times_are_not_mixed", "TypeError"),
    ),
    "round-1/25-rolling-analytics-window": (
        ("rolling_window.RollingWindowTests.test_aware_and_naive_timestamps_cannot_be_compared", "TypeError"),
    ),
}

# Return structured unittest results rather than interpreting a nonzero exit as
# an intentional failure. Redirect exercise output away from the JSON channel.
WORKER = r'''
import contextlib
import json
import sys
import unittest

class Result(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_details = []

    def addError(self, test, err):
        self.error_details.append((test.id(), err[0].__name__))
        super().addError(test, err)

    def addSubTest(self, test, subtest, err):
        if err is not None and not issubclass(err[0], test.failureException):
            self.error_details.append((subtest.id(), err[0].__name__))
        super().addSubTest(test, subtest, err)

with contextlib.redirect_stdout(sys.stderr):
    suite = unittest.defaultTestLoader.discover('.', pattern=sys.argv[1])
    result = unittest.TextTestRunner(resultclass=Result).run(suite)
print(json.dumps({
    'tests': result.testsRun,
    'failures': len(result.failures),
    'errors': result.error_details,
    'skipped': len(result.skipped),
    'expected_failures': len(result.expectedFailures),
    'unexpected_successes': len(result.unexpectedSuccesses),
}))
'''


def discover_exercises(root):
    """Require paired starters/solutions numbered 01 through 25 in each round."""
    exercises = []
    for round_name in ("round-1", "round-2"):
        paths = []
        for base in (root, root / "solutions"):
            directory = base / round_name
            names = sorted(
                path.name for path in directory.glob("[0-9][0-9]-*")
                if path.is_dir()
            )
            numbers = [name.split("-", 1)[0] for name in names]
            if numbers != [f"{number:02}" for number in range(1, 26)]:
                raise ValueError(f"{directory}: expected exercises 01 through 25 exactly once")
            paths.append(names)
        if paths[0] != paths[1]:
            raise ValueError(f"{round_name}: starter and solution directory names differ")
        exercises.extend(Path(round_name) / name for name in paths[0])
    return exercises


def run_suite(directory, pattern, *, starter=False, expected_errors=(), timeout=10):
    """Return (accepted, summary, captured diagnostics) for one isolated suite."""
    try:
        process = subprocess.run(
            [sys.executable, "-I", "-B", "-c", WORKER, pattern],
            cwd=directory, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout:g}s", ""
    output = process.stdout + process.stderr
    if process.returncode != 0:
        return False, f"suite process exited {process.returncode}", output
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError:
        return False, "suite did not return a unittest result", output
    summary = (
        f"{result['tests']} tests, {result['failures']} assertion failures, "
        f"{len(result['errors'])} runtime errors"
    )
    reason = None
    if result["tests"] == 0:
        reason = "no tests executed"
    elif result["skipped"] or result["expected_failures"] or result["unexpected_successes"]:
        reason = "skipped/expected-failure tests are not allowed"
    elif starter:
        unexpected = [tuple(error) for error in result["errors"] if tuple(error) not in expected_errors]
        if unexpected:
            reason = f"unexpected runtime errors: {unexpected}"
        elif not result["failures"] and not result["errors"]:
            reason = "starter unexpectedly passed"
    elif result["failures"] or result["errors"]:
        reason = "reference solution did not pass"
    return reason is None, summary + (f"; {reason}" if reason else ""), output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=10, help="seconds allowed per suite (default: 10)")
    args = parser.parse_args()
    if not 0 < args.timeout < float("inf"):
        parser.error("--timeout must be a finite positive number")
    root = Path(__file__).resolve().parent.parent
    try:
        exercises = discover_exercises(root)
    except ValueError as error:
        print(f"FAIL inventory: {error}", file=sys.stderr)
        return 1
    accepted = {"solution": 0, "starter": 0}
    for exercise in exercises:
        pattern = "*.py" if exercise.parts[0] == "round-1" else "test_*.py"
        for kind, base in (("solution", root / "solutions"), ("starter", root)):
            ok, summary, output = run_suite(
                base / exercise, pattern, starter=kind == "starter",
                expected_errors=EXPECTED_STARTER_ERRORS.get(exercise.as_posix(), ()),
                timeout=args.timeout,
            )
            accepted[kind] += int(ok)
            print(f"{'PASS' if ok else 'FAIL'} {kind} {exercise.as_posix()}: {summary}", flush=True)
            if not ok and output:
                print(output, file=sys.stderr, end="" if output.endswith("\n") else "\n")
    print(
        f"\nSolutions: {accepted['solution']}/50 passed; "
        f"starters: {accepted['starter']}/50 exposed expected defects."
    )
    return 0 if accepted == {"solution": 50, "starter": 50} else 1


if __name__ == "__main__":
    sys.exit(main())
