"""Aggregate grade rows while making batch retries safe."""

import unittest


def summarize_gradebook(rows):
    """Return per-student average and count from assessment rows."""
    totals = {}
    seen = set()
    for row in rows:
        student = row["student"].strip().casefold()
        assessment_id = row["assessment_id"]
        score = row["score"]
        key = (student, assessment_id)
        if key in seen:
            totals[student]["scores"].append(score)
        else:
            seen.add(key)
            totals.setdefault(student, {"name": row["student"].strip(), "scores": []})["scores"].append(score)
    return {
        data["name"]: {"count": len(data["scores"]), "average": round(sum(data["scores"]) / len(data["scores"]), 2)}
        for data in totals.values()
    }


class GradebookTests(unittest.TestCase):
    def test_distinct_assessments_contribute_to_average(self):
        rows = [{"student": "Ari", "assessment_id": "quiz-1", "score": 80},
                {"student": "Ari", "assessment_id": "quiz-2", "score": 100}]
        self.assertEqual(summarize_gradebook(rows), {"Ari": {"count": 2, "average": 90.0}})

    def test_replayed_batch_does_not_double_count_assessment(self):
        event = {"student": "Ari", "assessment_id": "quiz-1", "score": 80}
        self.assertEqual(summarize_gradebook([event, event]), {"Ari": {"count": 1, "average": 80.0}})

    def test_student_identity_is_trimmed_and_case_insensitive(self):
        rows = [{"student": " Jo ", "assessment_id": "q1", "score": 80},
                {"student": "jo", "assessment_id": "q2", "score": 100}]
        self.assertEqual(summarize_gradebook(rows), {"Jo": {"count": 2, "average": 90.0}})


if __name__ == "__main__":
    unittest.main()
