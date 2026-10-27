# PR #09 — Gradebook Batch Replay

**Difficulty:** Medium

## Practice Metadata

- **Interview format:** PR review / focused debugging.
- **Primary skills:** data aggregation, identity normalization, numeric reasoning.
- **Expected duration:** 45–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Compare the proposed change and its tests with the observable contract, then make a targeted correction and regression test.
- **Interviewer evaluation:** Clarifying questions, code investigation, root-cause reasoning, maintainable changes, testing, and communication. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

**PR title:** Ignore a repeated assessment import

## Summary

An instructor can import assessment scores in batches. If the import job retries after a timeout, rows from the same batch may arrive again. You are reviewing a change to the grade summary so a replay does not count the same student's assessment twice.

## Input and output

`summarize_gradebook(rows)` receives rows with a student name, an `assessment_id` unique for that student's assessment, and a numeric score. It returns each student's first trimmed display name with the number of distinct assessments and their average rounded to two decimal places. Student names differing only in surrounding whitespace or case identify the same student.

## Expected behavior

- Distinct assessment IDs for one student contribute once each.
- Repeating a row with the same student identity, assessment ID, and score is an import replay and contributes only once.
- Reusing an assessment ID for the same student with a different score is inconsistent input and raises `ValueError`.
- The result's count and average reflect distinct assessments only.

## Reproduction

Importing `{"student": "Ari", "assessment_id": "quiz-1", "score": 80}` twice must produce `{"Ari": {"count": 1, "average": 80.0}}`.

## Review task

Compare the import behavior and tests with replay and conflict semantics. Add a regression test that verifies both count and average after an exact replay, then explain why a conflicting replay must not silently change a published grade.

## Starter Code

[View starter code](../../round-1/09-gradebook-aggregation/)

## Reference Solution

[View solution](../../solutions/round-1/09-gradebook-aggregation/)
