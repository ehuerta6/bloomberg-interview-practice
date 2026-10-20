"""Rank search documents using query-term hits."""

import re
import unittest


def _terms(value):
    return re.findall(r"[a-z0-9]+", value.lower())


def rank_results(query, documents, limit=None):
    """Return matching document IDs with relevance scores, highest first."""
    query_terms = query.lower().split()
    ranked = []
    for index, document in enumerate(documents):
        title_terms = document["title"].lower().split()
        body_terms = document["text"].lower().split()
        title_hits = sum(term in title_terms for term in query_terms)
        body_hits = sum(term in body_terms for term in query_terms)
        score = (3 * title_hits + body_hits) / (4 * len(query_terms)) if query_terms else 0
        if score:
            ranked.append((score, index, document["id"]))
    ranked.sort(reverse=True)
    result = [{"id": doc_id, "score": round(score, 4)} for score, _, doc_id in ranked]
    return result[:limit] if limit is not None else result


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

    def test_query_matching_ignores_case_and_punctuation(self):
        self.assertEqual([row["id"] for row in rank_results("PYTHON!", self.documents)], ["title", "mixed", "body"])

    def test_each_query_term_contributes_to_score(self):
        self.assertEqual(rank_results("python guides", self.documents)[0]["id"], "title")

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
        self.assertEqual(rank_results("", self.documents), [])


if __name__ == "__main__":
    unittest.main()
