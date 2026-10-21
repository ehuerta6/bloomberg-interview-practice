# PR #09 — Gradebook Aggregation

**Difficulty:** Medium

**PR title:** Aggregate weighted assessment scores into student grades

## Summary

A course service combines assessment records across students and categories, applies category weights and a dropped-score policy, then returns one grade summary per student.

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

## Review task

Trace a student with multiple weighted categories and multiple input rows. Check per-category dropping, missing entries, empty-after-drop categories, total entry counts, rounding, and the letter-grade thresholds. Add focused tests for the contract's boundary cases.

## Starter Code

[View starter code](../../round-1/09-gradebook-aggregation/)

## Reference Solution

[View solution](../../solutions/round-1/09-gradebook-aggregation/)
