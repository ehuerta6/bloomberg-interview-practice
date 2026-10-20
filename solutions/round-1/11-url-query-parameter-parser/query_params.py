"""Parse URL query parameters, retaining decoded repeated values."""

import unittest
from urllib.parse import parse_qsl


def parse_query(query):
    """Return query keys mapped to ordered lists of decoded values."""
    if not isinstance(query, str):
        raise ValueError("query must be text")
    raw_query = query[1:] if query.startswith("?") else query
    result = {}
    for key, value in parse_qsl(raw_query, keep_blank_values=True, strict_parsing=False):
        result.setdefault(key, []).append(value)
    return result


class QueryParserTests(unittest.TestCase):
    def test_simple_pairs(self):
        self.assertEqual(parse_query("color=blue&page=2"), {"color": ["blue"], "page": ["2"]})

    def test_optional_question_mark(self):
        self.assertEqual(parse_query("?q=books"), {"q": ["books"]})

    def test_repeated_keys_preserve_order(self):
        self.assertEqual(parse_query("tag=a&tag=b"), {"tag": ["a", "b"]})

    def test_blank_values_and_bare_keys_are_kept(self):
        self.assertEqual(parse_query("flag&empty="), {"flag": [""], "empty": [""]})

    def test_only_first_equals_sign_separates_key_and_value(self):
        self.assertEqual(parse_query("redirect=a=b"), {"redirect": ["a=b"]})

    def test_percent_escapes_decode_in_keys_and_values(self):
        self.assertEqual(parse_query("q=red%20fox&%74ag=one"), {"q": ["red fox"], "tag": ["one"]})

    def test_plus_means_space(self):
        self.assertEqual(parse_query("q=red+fox"), {"q": ["red fox"]})

    def test_empty_segments_are_ignored(self):
        self.assertEqual(parse_query("&&a=1&&"), {"a": ["1"]})

    def test_empty_input_and_question_mark_have_no_parameters(self):
        self.assertEqual(parse_query(""), {})
        self.assertEqual(parse_query("?"), {})

    def test_non_text_input_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_query(None)


if __name__ == "__main__":
    unittest.main()
