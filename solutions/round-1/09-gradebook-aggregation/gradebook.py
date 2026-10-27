"""Aggregate grade rows while making batch retries safe."""

import unittest


def summarize_gradebook(rows):
    """Return per-student average and count, ignoring exact replayed rows."""
    students = {}
    seen = {}
    for row in rows:
        student = row["student"].strip()
        key = (student.casefold(), row["assessment_id"])
        if key in seen:
            if seen[key] != row["score"]:
                raise ValueError("an assessment ID has conflicting scores")
            continue
        seen[key] = row["score"]
        bucket = students.setdefault(key[0], {"name": student, "scores": []})
        bucket["scores"].append(row["score"])
    return {
        data["name"]: {"count": len(data["scores"]), "average": round(sum(data["scores"]) / len(data["scores"]), 2)}
        for data in students.values()
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

    def test_conflicting_replay_is_rejected(self):
        rows = [{"student": "Ari", "assessment_id": "quiz-1", "score": 80},
                {"student": "ari", "assessment_id": "quiz-1", "score": 90}]
        with self.assertRaises(ValueError):
            summarize_gradebook(rows)


if __name__ == "__main__":
    unittest.main()
