"""Rank documents by normalized title and body relevance."""

import re
from collections.abc import Mapping
import unittest


def _terms(value):
    return re.findall(r"[a-z0-9]+", value.casefold())


def rank_results(query, documents, limit=None):
    """Return ``{id, score}`` results in stable descending relevance order.

    Query terms are normalized alphanumeric tokens and counted once each.
    Each matching title term is worth three points; each matching body term is
    worth one. The score is normalized to a 0–1 range by the maximum possible
    four points per distinct query term. Documents with no matching terms are
    omitted. Equal scores retain input order.
    """
    if not isinstance(query, str):
        raise ValueError("query must be text")
    if not isinstance(documents, (list, tuple)):
        raise ValueError("documents must be a list or tuple")
    if limit is not None and (isinstance(limit, bool) or not isinstance(limit, int) or limit < 0):
        raise ValueError("limit must be a nonnegative integer or None")
    query_terms = set(_terms(query))
    if not query_terms or limit == 0:
        return []

    ranked = []
    for index, document in enumerate(documents):
        if not isinstance(document, Mapping):
            raise ValueError("each document must be a mapping")
        document_id = document.get("id")
        title = document.get("title")
        body = document.get("text")
        if document_id is None or not isinstance(title, str) or not isinstance(body, str):
            raise ValueError("each document needs an ID, title, and text")
        title_terms = set(_terms(title))
        body_terms = set(_terms(body))
        title_hits = len(query_terms & title_terms)
        body_hits = len(query_terms & body_terms)
        score = (3 * title_hits + body_hits) / (4 * len(query_terms))
        if score > 0:
            ranked.append((score, index, document_id))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    results = [{"id": document_id, "score": round(score, 4)} for score, _, document_id in ranked]
    return results if limit is None else results[:limit]


class SearchRankTests(unittest.TestCase):
    def setUp(self):
        self.documents = [
            {"id": "body", "title": "Notes", "text": "python guides"},
            {"id": "title", "title": "Python guides", "text": "language"},
            {"id": "mixed", "title": "Python", "text": "guides"},
            {"id": "other", "title": "Cooking", "text": "recipes"},
        ]

    def test_title_match_scores_higher_than_body_match(self):
        result = rank_results("python", self.documents)
        self.assertEqual([row["id"] for row in result[:2]], ["title", "mixed"])
        self.assertEqual(result[0]["score"], 0.75)

    def test_query_matching_normalizes_case_punctuation_and_repeated_terms(self):
        self.assertEqual(rank_results("PYTHON! python", self.documents)[0]["id"], "title")
        self.assertEqual(rank_results("PYTHON!", self.documents)[0]["score"], 0.75)

    def test_each_distinct_query_term_contributes_to_score(self):
        result = rank_results("python guides", self.documents)
        self.assertEqual(result[0], {"id": "title", "score": 0.75})
        self.assertEqual(result[1], {"id": "mixed", "score": 0.5})

    def test_ties_preserve_document_input_order(self):
        docs = [{"id": "first", "title": "python", "text": ""}, {"id": "second", "title": "python", "text": ""}]
        self.assertEqual([row["id"] for row in rank_results("python", docs)], ["first", "second"])

    def test_limit_truncates_ranked_results(self):
        self.assertEqual(len(rank_results("python", self.documents, limit=1)), 1)

    def test_zero_limit_returns_no_results(self):
        self.assertEqual(rank_results("python", self.documents, limit=0), [])

    def test_documents_without_matches_are_excluded(self):
        self.assertEqual([row["id"] for row in rank_results("python", self.documents)], ["title", "mixed", "body"])

    def test_empty_query_returns_no_results(self):
        self.assertEqual(rank_results("!!!", self.documents), [])

    def test_invalid_limit_and_document_shape_are_rejected(self):
        with self.assertRaises(ValueError):
            rank_results("python", self.documents, limit=True)
        with self.assertRaises(ValueError):
            rank_results("python", [{"id": "broken", "title": "python"}])


if __name__ == "__main__":
    unittest.main()
