"""Aggregate weighted assessment categories into student grade summaries."""

import unittest


def summarize_gradebook(rows, weights, drop_lowest=1):
    """Return a weighted category average for each student."""
    students = {}
    for row in rows:
        name = row["student"].strip()
        categories = row["scores"]
        students.setdefault(name, {})
        for category, scores in categories.items():
            students[name].setdefault(category, []).extend(scores)

    summaries = {}
    for name, categories in students.items():
        category_means = []
        count = 0
        for category in weights:
            scores = categories.get(category, [])
            count += len(scores)
            numeric_scores = [0 if score is None else score for score in scores]
            if numeric_scores:
                numeric_scores = sorted(numeric_scores)[drop_lowest:]
            category_means.append(sum(numeric_scores) / len(numeric_scores) if numeric_scores else 0)
        average = round(sum(category_means) / len(category_means), 2)
        letter = "A" if average >= 90 else "B" if average >= 80 else "C" if average >= 70 else "D" if average >= 60 else "F"
        summaries[name] = {"count": count, "average": average, "letter": letter}
    return summaries


class GradebookTests(unittest.TestCase):
    def test_weighted_categories_contribute_by_their_percentages(self):
        rows = [{"student": "Ari", "scores": {"exam": [100], "project": [0]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 80, "project": 20}, drop_lowest=0)["Ari"],
                         {"count": 2, "average": 80.0, "letter": "B"})

    def test_lowest_score_is_dropped_separately_in_each_category(self):
        rows = [{"student": "Bea", "scores": {"exam": [100, 90], "project": [80, 70]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 50, "project": 50})["Bea"]["average"], 90.0)

    def test_missing_score_is_zero_and_can_be_dropped(self):
        rows = [{"student": "Cal", "scores": {"exam": [100, None, 90]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 100})["Cal"],
                         {"count": 3, "average": 95.0, "letter": "A"})

    def test_category_emptied_by_dropping_contributes_zero(self):
        rows = [{"student": "Dee", "scores": {"exam": [85], "project": []}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 100})["Dee"]["average"], 0)

    def test_rows_merge_by_trimmed_casefolded_name_and_count_all_entries(self):
        rows = [{"student": " Jo ", "scores": {"exam": [100]}}, {"student": "jo", "scores": {"project": [80]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 50, "project": 50}, drop_lowest=0),
                         {"Jo": {"count": 2, "average": 90.0, "letter": "A"}})

    def test_rounding_does_not_change_letter_threshold(self):
        rows = [{"student": "Edge", "scores": {"exam": [89.995]}}]
        self.assertEqual(summarize_gradebook(rows, {"exam": 100}, drop_lowest=0)["Edge"],
                         {"count": 1, "average": 90.0, "letter": "B"})

    def test_grade_thresholds(self):
        rows = [{"student": str(score), "scores": {"exam": [score]}} for score in [90, 80, 70, 60, 59]]
        result = summarize_gradebook(rows, {"exam": 100}, drop_lowest=0)
        self.assertEqual([result[str(score)]["letter"] for score in [90, 80, 70, 60, 59]], ["A", "B", "C", "D", "F"])

    def test_score_boundaries_are_inclusive(self):
        result = summarize_gradebook([{"student": "Range", "scores": {"exam": [0, 100]}}], {"exam": 100}, drop_lowest=0)
        self.assertEqual(result["Range"]["average"], 50)

    def test_invalid_scores_are_rejected(self):
        for score in (101, -1, True, float("nan"), float("inf")):
            with self.subTest(score=score), self.assertRaises(ValueError):
                summarize_gradebook([{"student": "Pat", "scores": {"exam": [score]}}], {"exam": 100})

    def test_invalid_weights_and_category_names_are_rejected(self):
        rows = [{"student": "Pat", "scores": {"exam": [80]}}]
        for weights in ({"exam": 90}, {"": 100}, {"exam": True}, []):
            with self.subTest(weights=weights), self.assertRaises(ValueError):
                summarize_gradebook(rows, weights)

    def test_unknown_categories_and_bad_drop_counts_are_rejected(self):
        for rows, drop in (([{"student": "Pat", "scores": {"quiz": [80]}}], 0),
                           ([{"student": "Pat", "scores": {"exam": [80]}}], True),
                           ([{"student": "Pat", "scores": {"exam": [80]}}], -1)):
            with self.subTest(rows=rows, drop=drop), self.assertRaises(ValueError):
                summarize_gradebook(rows, {"exam": 100}, drop_lowest=drop)


if __name__ == "__main__":
    unittest.main()
