"""Parse and validate account rows from a CSV export."""

import csv
import io
import unittest


EXPECTED_HEADER = ["user_id", "email", "active"]


def parse_users(text):
    """Return normalized user dictionaries from CSV text.

    Blank lines are ignored. IDs are kept as strings, email values are
    case-folded, and active values must be the words true or false.
    """
    if not isinstance(text, str):
        raise ValueError("CSV input must be text")
    reader = csv.reader(io.StringIO(text, newline=""), skipinitialspace=True, strict=True)
    try:
        header = next((row for row in reader if any(cell.strip() for cell in row)), None)
    except csv.Error as exc:
        raise ValueError("malformed CSV document") from exc
    if header is None or [cell.strip() for cell in header] != EXPECTED_HEADER:
        raise ValueError("unexpected CSV header")

    users = []
    seen_ids = set()
    try:
        rows = list(reader)
    except csv.Error as exc:
        raise ValueError("malformed CSV document") from exc
    for fields in rows:
        if not fields or not any(field.strip() for field in fields):
            continue
        if len(fields) != 3:
            raise ValueError("each row must have three fields")
        user_id, email, active = (field.strip() for field in fields)
        active_value = active.casefold()
        if not user_id or not email or "@" not in email:
            raise ValueError("user ID and a valid email are required")
        if active_value not in {"true", "false"}:
            raise ValueError("active must be true or false")
        if user_id in seen_ids:
            raise ValueError("user IDs must be unique")
        seen_ids.add(user_id)
        users.append({"user_id": user_id, "email": email.casefold(), "active": active_value == "true"})
    return users


class CsvImportTests(unittest.TestCase):
    def test_basic_rows_are_normalized(self):
        self.assertEqual(parse_users("user_id,email,active\n7,ADA@EXAMPLE.COM,true"), [{"user_id": "7", "email": "ada@example.com", "active": True}])

    def test_true_and_false_are_parsed_explicitly(self):
        result = parse_users("user_id,email,active\n7,a@example.com,true\n8,b@example.com,false")
        self.assertEqual([row["active"] for row in result], [True, False])

    def test_quoted_comma_and_escaped_quote_are_preserved(self):
        result = parse_users('user_id,email,active\n9,"lee, ""jr""@example.com",true')
        self.assertEqual(result[0]["email"], 'lee, "jr"@example.com')

    def test_header_whitespace_and_blank_lines_are_ignored(self):
        result = parse_users("\nuser_id, email, active\n\n1, a@example.com, TRUE\n")
        self.assertEqual(result[0]["user_id"], "1")
        self.assertTrue(result[0]["active"])

    def test_wrong_header_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_users("id,email,active\n1,a@example.com,true")

    def test_wrong_width_and_invalid_boolean_are_rejected(self):
        for document in ("user_id,email,active\n1,a@example.com", "user_id,email,active\n1,a@example.com,yes"):
            with self.subTest(document=document), self.assertRaises(ValueError):
                parse_users(document)

    def test_duplicate_ids_and_missing_identity_fields_are_rejected(self):
        documents = ("user_id,email,active\n1,a@example.com,true\n1,b@example.com,false", "user_id,email,active\n,a@example.com,true", "user_id,email,active\n1,,true")
        for document in documents:
            with self.subTest(document=document), self.assertRaises(ValueError):
                parse_users(document)

    def test_crlf_and_quoted_line_break_are_supported(self):
        result = parse_users('user_id,email,active\r\n1,"a\r\nb@example.com",false\r\n')
        self.assertEqual(result[0]["email"], "a\r\nb@example.com")
        self.assertFalse(result[0]["active"])

    def test_empty_document_and_malformed_quotes_are_rejected(self):
        for document in ("", 'user_id,email,active\n1,"broken,true'):
            with self.subTest(document=document), self.assertRaises(ValueError):
                parse_users(document)


if __name__ == "__main__":
    unittest.main()
