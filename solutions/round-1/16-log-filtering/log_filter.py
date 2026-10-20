"""Filter structured logs by severity and inclusive timestamp range."""

import math
from collections.abc import Mapping
import unittest


SEVERITIES = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
SEVERITY_RANK = {name: rank for rank, name in enumerate(SEVERITIES)}


def _finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def filter_logs(entries, minimum_severity="INFO", start_time=None, end_time=None):
    """Return well-formed entries meeting the severity and inclusive time bounds.

    Malformed log records are ignored. Invalid filter arguments raise
    ``ValueError``. The returned dictionaries are the original entries in
    their original order.
    """
    if not isinstance(entries, (list, tuple)):
        raise ValueError("entries must be a list or tuple")
    if not isinstance(minimum_severity, str) or minimum_severity.upper() not in SEVERITY_RANK:
        raise ValueError("unknown minimum severity")
    if start_time is not None and not _finite_number(start_time):
        raise ValueError("start_time must be a finite number")
    if end_time is not None and not _finite_number(end_time):
        raise ValueError("end_time must be a finite number")
    if start_time is not None and end_time is not None and start_time > end_time:
        raise ValueError("start_time must not exceed end_time")

    threshold = SEVERITY_RANK[minimum_severity.upper()]
    accepted = []
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        timestamp = entry.get("timestamp")
        severity = entry.get("severity")
        if not _finite_number(timestamp) or not isinstance(severity, str):
            continue
        rank = SEVERITY_RANK.get(severity.upper())
        if rank is None:
            continue
        if start_time is not None and timestamp < start_time:
            continue
        if end_time is not None and timestamp > end_time:
            continue
        if rank >= threshold:
            accepted.append(entry)
    return accepted


class LogFilterTests(unittest.TestCase):
    def setUp(self):
        self.entries = [
            {"timestamp": 1, "severity": "DEBUG", "message": "start"},
            {"timestamp": 2, "severity": "INFO", "message": "ready"},
            {"timestamp": 3, "severity": "WARNING", "message": "slow"},
            {"timestamp": 4, "severity": "ERROR", "message": "failed"},
        ]

    def test_minimum_severity_includes_higher_levels(self):
        self.assertEqual([item["severity"] for item in filter_logs(self.entries, "WARNING")], ["WARNING", "ERROR"])

    def test_severity_names_are_case_insensitive(self):
        self.assertEqual(len(filter_logs(self.entries, "error")), 1)

    def test_start_and_end_bounds_are_inclusive(self):
        self.assertEqual([item["timestamp"] for item in filter_logs(self.entries, "DEBUG", 2, 3)], [2, 3])

    def test_time_range_and_severity_filter_compose(self):
        self.assertEqual([item["severity"] for item in filter_logs(self.entries, "INFO", 2, 4)], ["INFO", "WARNING", "ERROR"])

    def test_unknown_entry_severity_is_skipped(self):
        entries = self.entries + [{"timestamp": 5, "severity": "TRACE", "message": "extra"}]
        self.assertEqual(len(filter_logs(entries, "DEBUG")), 4)

    def test_malformed_entries_are_skipped(self):
        entries = [self.entries[0], {"message": "missing fields"}, {"timestamp": "later", "severity": "ERROR"}, None]
        self.assertEqual(filter_logs(entries, "DEBUG"), [self.entries[0]])

    def test_open_ended_ranges_work(self):
        self.assertEqual([item["timestamp"] for item in filter_logs(self.entries, "DEBUG", end_time=2)], [1, 2])
        self.assertEqual([item["timestamp"] for item in filter_logs(self.entries, "DEBUG", start_time=3)], [3, 4])

    def test_invalid_filter_arguments_are_rejected(self):
        for args in (("TRACE", None, None), ("INFO", 4, 2), ("INFO", float("nan"), None), ("INFO", None, True)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                filter_logs(self.entries, args[0], args[1], args[2])

    def test_empty_logs_return_empty_list(self):
        self.assertEqual(filter_logs([], "INFO"), [])


if __name__ == "__main__":
    unittest.main()
