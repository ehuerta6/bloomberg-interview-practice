"""Parse account rows from a small CSV export."""

import unittest


EXPECTED_HEADER = ["user_id", "email", "active"]


def parse_users(text):
    """Convert a CSV document into normalized user dictionaries."""
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines or lines[0].split(",") != EXPECTED_HEADER:
        raise ValueError("unexpected CSV header")
    users = []
    for line in lines[1:]:
        fields = [field.strip() for field in line.split(",")]
        if len(fields) != 3:
            raise ValueError("each row must have three fields")
        users.append({"user_id": fields[0], "email": fields[1].lower(), "active": bool(fields[2])})
    return users


class CsvImportTests(unittest.TestCase):
    def test_basic_rows_are_normalized(self):
        self.assertEqual(parse_users("user_id,email,active\n7,ADA@EXAMPLE.COM,true"),
                         [{"user_id": "7", "email": "ada@example.com", "active": True}])

    def test_false_is_parsed_as_false(self):
        self.assertFalse(parse_users("user_id,email,active\n8,b@example.com,false")[0]["active"])

    def test_quoted_comma_in_email_display_value_is_preserved(self):
        parsed = parse_users('user_id,email,active\n9,"lee, jr@example.com",true')
        self.assertEqual(parsed[0]["email"], "lee, jr@example.com")

    def test_header_whitespace_is_ignored(self):
        self.assertEqual(parse_users("user_id, email, active\n1, a@example.com, true")[0]["user_id"], "1")

    def test_blank_lines_are_skipped(self):
        self.assertEqual(len(parse_users("user_id,email,active\n\n1,a@example.com,true\n")), 1)

    def test_wrong_header_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_users("id,email,active\n1,a@example.com,true")

    def test_short_row_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_users("user_id,email,active\n1,a@example.com")

    def test_duplicate_user_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            parse_users("user_id,email,active\n1,a@example.com,true\n1,b@example.com,false")


if __name__ == "__main__":
    unittest.main()
