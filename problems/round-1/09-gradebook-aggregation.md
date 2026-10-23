# PR #09 — Gradebook Aggregation

**Difficulty:** Medium

**PR title:** Aggregate weighted assessment scores into student grades

## Summary

A course publishes a final grade for each student from assessment records submitted in several batches. Exams and projects can have different weights, and the course may drop low scores within each category. You are reviewing the PR that combines those records into a grade summary while retaining the number of input entries for reporting.

## Input and output

`summarize_gradebook(rows, weights, drop_lowest=1)` accepts rows containing a `student` name and a `scores` mapping from category name to a list of percentage scores. `weights` maps each category name to its percentage weight. It returns a mapping from the first trimmed student spelling to a summary with `count`, `average`, and `letter`.

## Expected behavior and invariants
- Merge rows whose trimmed student names match without regard to case; keep the first trimmed spelling as the output key.
- Weights must be a nonempty mapping of nonblank category names to finite, non-boolean percentages from 0 through 100, totaling 100. Row categories must be included in that mapping.
- Each category value is a score list. Every entry is a finite, non-boolean percentage from 0 through 100 or `None`. `None` represents a missing submission and contributes a score of zero.
- Drop `drop_lowest` lowest entries from each student's category after merging rows. The drop count is a nonnegative integer and includes zero-valued or missing entries. If no entries remain, that category contributes a mean of zero.
- Combine category means using their percentage weights. `count` is the total number of entries before dropping, including missing and later-dropped entries.
- Round the final average to two decimal places. Assign letters from the unrounded average: A at 90, B at 80, C at 70, D at 60, and F below 60.
- Reject malformed row/category/weight shapes, invalid scores, and invalid drop counts with `ValueError`.

## Contract examples

For this input, with `weights={"exam": 80, "project": 20}` and `drop_lowest=0`:

```python
[{"student": "Ari", "scores": {"exam": [100], "project": [0]}}]
```

The expected return is `{"Ari": {"count": 2, "average": 80.0, "letter": "B"}}`: the two category percentages contribute according to their weights.

For `[{"student": "Cal", "scores": {"exam": [100, None, 90]}}]`, `weights={"exam": 100}`, and the default drop count of 1, the expected summary for Cal is `{"count": 3, "average": 95.0, "letter": "A"}`. The missing entry counts toward `count` even though it is dropped.

An unrounded average of `89.995` displays as `90.0` but receives letter `"B"`.

## Review task

Review the aggregation and assertions against weighted grades, merged student identities, and the drop policy. Correct discrepancies and add cases that check all three summary fields, including missing submissions and a displayed average near a letter boundary. Explain how the tests distinguish the displayed number from the grade decision.

## Starter Code

[View starter code](../../round-1/09-gradebook-aggregation/)

## Reference Solution

[View solution](../../solutions/round-1/09-gradebook-aggregation/)
