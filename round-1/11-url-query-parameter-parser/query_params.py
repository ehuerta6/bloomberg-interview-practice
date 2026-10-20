"""Parse a URL query string into a mapping of keys to values."""

import unittest


def parse_query(query):
    """Return a dictionary whose values are lists, preserving repeated keys."""
    query = query[1:] if query.startswith("?") else query
    result = {}
    for part in query.split("&"):
        if not part:
            continue
        key, separator, value = part.partition("=")
        if not separator:
            value = ""
        result.setdefault(key, []).append(value)
    return result


class QueryParserTests(unittest.TestCase):
    def test_simple_pairs(self):
        self.assertEqual(parse_query("color=blue&page=2"), {"color": ["blue"], "page": ["2"]})

    def test_optional_question_mark(self):
        self.assertEqual(parse_query("?q=books"), {"q": ["books"]})

    def test_repeated_keys_preserve_order(self):
        self.assertEqual(parse_query("tag=a&tag=b"), {"tag": ["a", "b"]})

    def test_blank_values_are_kept(self):
        self.assertEqual(parse_query("flag&empty="), {"flag": [""], "empty": [""]})

    def test_only_first_equals_sign_separates_key_and_value(self):
        self.assertEqual(parse_query("redirect=a=b"), {"redirect": ["a=b"]})

    def test_percent_escapes_are_decoded(self):
        self.assertEqual(parse_query("q=red%20fox"), {"q": ["red fox"]})

    def test_plus_means_space(self):
        self.assertEqual(parse_query("q=red+fox"), {"q": ["red fox"]})

    def test_empty_input_has_no_parameters(self):
        self.assertEqual(parse_query(""), {})


if __name__ == "__main__":
    unittest.main()
