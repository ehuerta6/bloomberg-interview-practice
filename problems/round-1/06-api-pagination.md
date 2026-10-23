# PR #06 — API Pagination

**Difficulty:** Hard

**PR title:** Add stable keyset pagination to the records endpoint

## Summary

A records endpoint must let a client continue browsing as records change between requests. Each record has a unique string `id`, integer `created_at`, and optional integer `version`. Results from separate data partitions can overlap, so the same ID may occur more than once. You are reviewing the pagination PR, including the rule for continuing after a record has been deleted. A cursor is a position in the ordered results, represented by `(created_at, id)`.

## Expected behavior
- `paginate(records, cursor=None, limit=2)` returns `(page, next_cursor)`. The limit is a positive integer, not a boolean.
- Rows missing a nonblank string ID or integer timestamp are skipped. For duplicate IDs, retain the row with the greatest version; equal versions retain the first row.
- Sort by `(created_at, id)`. A cursor is that same tuple, and the next page contains only rows with a strictly greater key.
- The next cursor is the final row's key only when additional rows remain. An empty or final page returns `None`.
- A cursor remains useful even if its original record is no longer present.

## Contract example

The input records are:

```python
[
    {"id": "b", "created_at": 10, "version": 1},
    {"id": "a", "created_at": 10, "version": 1},
    {"id": "c", "created_at": 20, "version": 1},
]
```

With `limit=2`, the first call returns records `a`, `b` in that order and cursor `(10, "b")`. A call with that cursor returns only `c` and cursor `None`. If record `b` has been removed before the second call, the expected second page is still only `c`.

If an additional row for `a` has `created_at=5` and `version=2`, a full page contains `a` version 2, `b` version 1, then `c` version 1.

## Review task

Review the implementation and assertions against the page contents, ordering, and continuation contract. Add regression coverage for equal timestamps, duplicate versions, a deleted boundary record, invalid limits, and the final page. Explain why the results demonstrate that records are neither repeated nor skipped at a page boundary.

## Starter Code

[View starter code](../../round-1/06-api-pagination/)

## Reference Solution

[View solution](../../solutions/round-1/06-api-pagination/)
