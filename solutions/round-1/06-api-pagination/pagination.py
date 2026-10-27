"""Paginate a changing records feed using a compound key."""

import unittest


def paginate(records, cursor=None, limit=2):
    """Return a page and its continuation cursor (created_at, id)."""
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be a positive integer")
    ordered = sorted(records, key=lambda record: (record["created_at"], record["id"]))
    if cursor is not None:
        ordered = [record for record in ordered if (record["created_at"], record["id"]) > cursor]
    page = ordered[:limit]
    next_cursor = (page[-1]["created_at"], page[-1]["id"]) if len(ordered) > limit else None
    return page, next_cursor


class PaginationTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"id": "b", "created_at": 10},
            {"id": "a", "created_at": 10},
            {"id": "c", "created_at": 20},
        ]

    def test_first_page_orders_equal_timestamps_by_id(self):
        page, cursor = paginate(self.records, limit=2)
        self.assertEqual([row["id"] for row in page], ["a", "b"])
        self.assertEqual(cursor, (10, "b"))

    def test_next_page_continues_after_the_cursor(self):
        page, next_cursor = paginate(self.records, cursor=(10, "b"), limit=2)
        self.assertEqual([row["id"] for row in page], ["c"])
        self.assertIsNone(next_cursor)

    def test_deleted_cursor_still_resumes_at_the_next_sort_key(self):
        records = [row for row in self.records if row["id"] != "b"]
        page, _ = paginate(records, cursor=(10, "b"), limit=2)
        self.assertEqual([row["id"] for row in page], ["c"])

    def test_invalid_limit_is_rejected(self):
        for limit in (0, True):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                paginate(self.records, limit=limit)


if __name__ == "__main__":
    unittest.main()
