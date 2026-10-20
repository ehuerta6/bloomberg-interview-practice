"""Reference keyset pagination with deterministic normalization and tests."""

import unittest


def _valid_record(record):
    return (
        isinstance(record, dict)
        and isinstance(record.get("id"), str)
        and bool(record["id"].strip())
        and isinstance(record.get("created_at"), int)
        and not isinstance(record.get("created_at"), bool)
        and isinstance(record.get("version", 0), int)
        and not isinstance(record.get("version", 0), bool)
    )


def paginate(records, cursor=None, limit=2):
    """Return (page, next_cursor), using a deletion-safe (time, id) cursor."""
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be a positive integer")
    if cursor is not None and (
        not isinstance(cursor, tuple)
        or len(cursor) != 2
        or isinstance(cursor[0], bool)
        or not isinstance(cursor[0], int)
        or not isinstance(cursor[1], str)
    ):
        raise ValueError("cursor must be a (created_at, id) tuple")

    by_id = {}
    for record in records:
        if not _valid_record(record):
            continue
        current = by_id.get(record["id"])
        if current is None or record.get("version", 0) > current.get("version", 0):
            by_id[record["id"]] = record

    ordered = sorted(by_id.values(), key=lambda row: (row["created_at"], row["id"]))
    if cursor is not None:
        ordered = [row for row in ordered if (row["created_at"], row["id"]) > cursor]

    page = ordered[:limit]
    next_cursor = (page[-1]["created_at"], page[-1]["id"]) if len(ordered) > limit else None
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
        self.assertEqual([(row["id"], row["version"]) for row in page], [("a", 2), ("b", 1), ("c", 1)])

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

    def test_malformed_cursor_is_rejected(self):
        with self.assertRaises(ValueError):
            paginate(self.records, cursor="b")

    def test_equal_versions_keep_first_source_row(self):
        first = {"id": "a", "created_at": 1, "version": 4, "value": "first"}
        second = {"id": "a", "created_at": 2, "version": 4, "value": "second"}
        page, _ = paginate([first, second], limit=1)
        self.assertEqual(page[0]["value"], "first")


if __name__ == "__main__":
    unittest.main()
