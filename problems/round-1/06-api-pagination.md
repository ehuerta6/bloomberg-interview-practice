# PR #06 — API Pagination

**Difficulty:** Hard

**PR title:** Add stable keyset pagination to the records endpoint

## Summary

The endpoint returns a bounded page of records from a changing data source. Records have a unique string `id`, integer `created_at`, and optional integer `version`. Shards can overlap, and a record used to create a previous-page cursor may be deleted before the next request.

## Expected behavior
- `paginate(records, cursor=None, limit=2)` returns `(page, next_cursor)`. The limit is a positive integer, not a boolean.
- Rows missing a nonblank string ID or integer timestamp are skipped. For duplicate IDs, retain the row with the greatest version; equal versions retain the first row.
- Sort by `(created_at, id)`. A cursor is that same tuple, and the next page contains only rows with a strictly greater key.
- The next cursor is the final row's key only when additional rows remain. An empty or final page returns `None`.
- A cursor remains useful even if its original record is no longer present.

## Review task

Trace two pages across tied timestamps, duplicate IDs, and a deleted cursor row. Check whether pagination depends on locating a previous record in the current snapshot and whether all sort columns are represented in the cursor.

## Starter Code

[View starter code](../../round-1/06-api-pagination/)

## Reference Solution

[View solution](../../solutions/round-1/06-api-pagination/)
