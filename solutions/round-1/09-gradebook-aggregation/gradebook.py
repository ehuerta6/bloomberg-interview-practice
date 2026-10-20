"""Aggregate weighted assessment categories into student grade summaries."""

import math
from collections.abc import Mapping
import unittest


def _finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def summarize_gradebook(rows, weights, drop_lowest=1):
    """Summarize rows using weighted category means and per-category drops.

    Each row contains a student name and a category-to-list mapping. ``None``
    is a missing submission and counts as a zero. The requested number of
    lowest entries is dropped independently within each category after rows
    have been combined. The output count includes all input entries, including
    missing entries and entries later dropped.
    """
    if not isinstance(rows, (list, tuple)):
        raise ValueError("rows must be a list or tuple")
    if not isinstance(weights, Mapping) or not weights:
        raise ValueError("weights must be a nonempty category mapping")
    if isinstance(drop_lowest, bool) or not isinstance(drop_lowest, int) or drop_lowest < 0:
        raise ValueError("drop_lowest must be a nonnegative integer")

    normalized_weights = {}
    for category, weight in weights.items():
        if not isinstance(category, str) or not category.strip():
            raise ValueError("category names must be nonblank strings")
        if not _finite_number(weight) or not 0 <= weight <= 100:
            raise ValueError("weights must be finite percentages from 0 through 100")
        normalized_weights[category] = weight
    if not math.isclose(sum(normalized_weights.values()), 100.0, rel_tol=0, abs_tol=1e-9):
        raise ValueError("category weights must total 100")

    students = {}
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("each row must be a mapping")
        name = row.get("student")
        categories = row.get("scores")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("student names must be nonblank strings")
        if not isinstance(categories, Mapping):
            raise ValueError("scores must map categories to score lists")
        unknown = set(categories) - set(normalized_weights)
        if unknown:
            raise ValueError("score category is missing from weights")
        key_name = name.strip()
        key = key_name.casefold()
        student = students.setdefault(key, {"name": key_name, "scores": {}})
        for category, scores in categories.items():
            if not isinstance(scores, (list, tuple)):
                raise ValueError("each category must contain a score list")
            destination = student["scores"].setdefault(category, [])
            for score in scores:
                if score is not None and (not _finite_number(score) or not 0 <= score <= 100):
                    raise ValueError("scores must be None or finite percentages from 0 through 100")
                destination.append(0 if score is None else score)

    summaries = {}
    for student in students.values():
        weighted_average = 0.0
        count = 0
        for category, weight in normalized_weights.items():
            scores = student["scores"].get(category, [])
            count += len(scores)
            kept = sorted(scores)[drop_lowest:]
            category_mean = sum(kept) / len(kept) if kept else 0.0
            weighted_average += category_mean * weight / 100
        letter = "A" if weighted_average >= 90 else "B" if weighted_average >= 80 else "C" if weighted_average >= 70 else "D" if weighted_average >= 60 else "F"
        summaries[student["name"]] = {
            "count": count,
            "average": round(weighted_average, 2),
            "letter": letter,
        }
    return summaries


class GradebookTests(unittest.TestCase):
    def test_weighted_categories_contribute_by_their_percentages(self):
        rows = [{"student": "Ari", "scores": {"exam": [100], "project": [0]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 80, "project": 20}, drop_lowest=0)["Ari"], {"count": 2, "average": 80.0, "letter": "B"})

    def test_lowest_score_is_dropped_separately_in_each_category(self):
        rows = [{"student": "Bea", "scores": {"exam": [100, 90], "project": [80, 70]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 50, "project": 50})["Bea"], {"count": 4, "average": 90.0, "letter": "A"})

    def test_missing_entry_counts_as_zero_and_can_be_dropped(self):
        rows = [{"student": "Cal", "scores": {"exam": [100, None, 90]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 100})["Cal"], {"count": 3, "average": 95.0, "letter": "A"})

    def test_empty_category_after_dropping_contributes_zero(self):
        rows = [{"student": "Dee", "scores": {"exam": [85]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 100})["Dee"], {"count": 1, "average": 0.0, "letter": "F"})

    def test_missing_category_contributes_zero(self):
        rows = [{"student": "Eli", "scores": {"exam": [100]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 50, "project": 50}, drop_lowest=0)["Eli"]["average"], 50.0)

    def test_rows_merge_by_trimmed_casefolded_name_and_keep_first_spelling(self):
        rows = [{"student": " Jo ", "scores": {"exam": [100]}}, {"student": "jo", "scores": {"project": [80]}}]
        result = summarize_gradebook(rows, {"exam": 50, "project": 50}, drop_lowest=0)
        self.assertEqual(result, {"Jo": {"count": 2, "average": 90.0, "letter": "A"}})

    def test_rounding_does_not_change_letter_threshold(self):
        rows = [{"student": "Edge", "scores": {"exam": [89.995]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 100}, drop_lowest=0)["Edge"], {"count": 1, "average": 90.0, "letter": "B"})

    def test_all_grade_thresholds(self):
        rows = [{"student": str(score), "scores": {"exam": [score]}} for score in [90, 80, 70, 60, 59]]
        result = summarize_gradebook(rows, {"exam": 100}, drop_lowest=0)
        self.assertEqual([result[str(score)]["letter"] for score in [90, 80, 70, 60, 59]], ["A", "B", "C", "D", "F"])

    def test_empty_input_returns_empty_mapping(self):
        self.assertEqual(summarize_gradebook([], {"exam": 100}), {})

    def test_invalid_score_values_are_rejected(self):
        for score in (101, -1, True, float("nan"), float("inf")):
            with self.subTest(score=score), self.assertRaises(ValueError):
                summarize_gradebook([{"student": "Pat", "scores": {"exam": [score]}}], {"exam": 100})

    def test_invalid_weights_are_rejected(self):
        for weights in ({"exam": 90}, {"exam": True}, {"exam": float("inf")}, {}, []):
            with self.subTest(weights=weights), self.assertRaises(ValueError):
                summarize_gradebook([], weights)

    def test_invalid_categories_rows_and_drop_counts_are_rejected(self):
        examples = (
            ([{"student": "Pat", "scores": {"quiz": [80]}}], {"exam": 100}, 0),
            ([{"student": "Pat", "scores": {"exam": 80}}], {"exam": 100}, 0),
            ([{"student": "  ", "scores": {}}], {"exam": 100}, 0),
            ([{"student": "Pat", "scores": {"exam": [80]}}], {"exam": 100}, True),
        )
        for rows, weights, drop in examples:
            with self.subTest(rows=rows, weights=weights, drop=drop), self.assertRaises(ValueError):
                summarize_gradebook(rows, weights, drop_lowest=drop)


if __name__ == "__main__":
    unittest.main()
