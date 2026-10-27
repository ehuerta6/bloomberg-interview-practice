# PR #06 — API Pagination

**Difficulty:** Medium

## Practice Metadata

- **Interview format:** PR review / focused debugging.
- **Primary skills:** cursor invariants, stable ordering, regression testing.
- **Expected duration:** 45–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Compare the proposed change and its tests with the observable contract, then make a targeted correction and regression test.
- **Interviewer evaluation:** Clarifying questions, code investigation, root-cause reasoning, maintainable changes, testing, and communication. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

**PR title:** Continue record feeds without repeating or skipping rows

## Summary

A client reads a records feed in pages while new records may be written between requests. The endpoint orders records by creation time, but several records can share the same timestamp. You are reviewing a keyset-pagination change after clients reported repeated rows at a page boundary.

## Input and output

`paginate(records, cursor=None, limit=2)` returns `(page, next_cursor)`. Each record has a unique string `id` and integer `created_at`. Results are ordered by `(created_at, id)`, and the cursor is the same pair. `limit` must be a positive integer and cannot be a boolean.

## Expected behavior

- The first page is the first `limit` records in compound-key order.
- A later page contains only records whose compound key is strictly greater than the supplied cursor. The cursor's record may have been deleted.
- Return the last page record's compound key only when additional records remain; otherwise return `None`.
- Do not repeat or skip a record solely because timestamps are equal.

## Reproduction

For records `b@10`, `a@10`, and `c@20`, a page of two returns `a`, `b` and cursor `(10, "b")`. Continuing with that cursor returns only `c`. If `b` was deleted between requests, continuation still returns `c`.

## Review task

Trace how sorting and cursor comparison interact. Add or refine tests for equal timestamps, the next page, and continuation after deletion. Explain what the compound key guarantees and what can still change when records are inserted during pagination.

## Starter Code

[View starter code](../../round-1/06-api-pagination/)

## Reference Solution

[View solution](../../solutions/round-1/06-api-pagination/)
