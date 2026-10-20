"""Keyset pagination for an API result set and its review tests."""

import unittest


def paginate(records, cursor=None, limit=2):
    """Return (page, next_cursor), where cursors are (created_at, id) tuples."""
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be a positive integer")

    ordered = sorted(
        (record for record in records if record.get("id") and isinstance(record.get("created_at"), int)),
        key=lambda record: record["created_at"],
    )
    start = 0
    if cursor is not None:
        for index, record in enumerate(ordered):
            if record["id"] == cursor:
                start = index + 1
                break

    page = ordered[start:start + limit]
    next_cursor = page[-1]["id"] if start + limit < len(ordered) and page else None
    return page, next_cursor


class PaginationTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"id": "b", "created_at": 10, "version": 1},
            {"id": "a", "created_at": 10, "version": 1},
            {"id": "c", "created_at": 20, "version": 1},
        ]

    def test_first_page_is_ordered_stably_by_time_then_id(self):
        page, cursor = paginate(self.records, limit=2)
        self.assertEqual([row["id"] for row in page], ["a", "b"])
        self.assertEqual(cursor, (10, "b"))

    def test_next_page_starts_after_compound_cursor(self):
        page, cursor = paginate(self.records, cursor=(10, "b"), limit=2)
        self.assertEqual([row["id"] for row in page], ["c"])
        self.assertIsNone(cursor)

    def test_deleted_cursor_still_resumes_by_sort_key(self):
        remaining = [row for row in self.records if row["id"] != "b"]
        page, _ = paginate(remaining, cursor=(10, "b"), limit=2)
        self.assertEqual([row["id"] for row in page], ["c"])

    def test_duplicate_id_keeps_highest_version(self):
        rows = self.records + [{"id": "a", "created_at": 5, "version": 2}]
        page, _ = paginate(rows, limit=5)
        self.assertEqual([(row["id"], row["version"]) for row in page], [("b", 1), ("a", 2), ("c", 1)])

    def test_malformed_records_are_skipped(self):
        page, _ = paginate(self.records + [{"created_at": 1}, {"id": "x", "created_at": "now"}], limit=5)
        self.assertEqual(len(page), 3)

    def test_empty_result_has_no_cursor(self):
        self.assertEqual(paginate([], limit=2), ([], None))

    def test_zero_limit_is_rejected(self):
        with self.assertRaises(ValueError):
            paginate(self.records, limit=0)

    def test_boolean_limit_is_rejected(self):
        with self.assertRaises(ValueError):
            paginate(self.records, limit=True)


if __name__ == "__main__":
    unittest.main()
