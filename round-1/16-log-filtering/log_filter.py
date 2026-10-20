"""Filter structured log entries by severity and timestamp."""

import unittest


SEVERITIES = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def filter_logs(entries, minimum_severity="INFO", start_time=None, end_time=None):
    """Return entries at or above a severity threshold and within a time range."""
    threshold = SEVERITIES.index(minimum_severity.upper())
    result = []
    for entry in entries:
        timestamp = entry["timestamp"]
        severity = entry["severity"].upper()
        if severity not in SEVERITIES:
            continue
        if start_time is not None and timestamp <= start_time:
            continue
        if end_time is not None and timestamp >= end_time:
            continue
        if SEVERITIES.index(severity) >= threshold:
            result.append(entry)
    return result


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
        entries = [self.entries[0], {"message": "missing fields"}, {"timestamp": "later", "severity": "ERROR"}]
        self.assertEqual(filter_logs(entries, "DEBUG"), [self.entries[0]])

    def test_invalid_filter_arguments_are_rejected(self):
        with self.assertRaises(ValueError):
            filter_logs(self.entries, "TRACE")

    def test_empty_logs_return_empty_list(self):
        self.assertEqual(filter_logs([], "INFO"), [])


if __name__ == "__main__":
    unittest.main()
