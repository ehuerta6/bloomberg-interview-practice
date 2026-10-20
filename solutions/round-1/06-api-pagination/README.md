# API Pagination — Reference Solution

## What was broken

The draft sorted only by timestamp, used the last record's ID as a cursor, and restarted from the beginning if that ID was absent. Equal timestamps could move between pages depending on source order, duplicate IDs could appear twice, and deleting the cursor row could repeat earlier results.

## Reproduce the issue

Run `python3 pagination.py` in the starter directory. The tuple cursor and deleted-row tests fail because the implementation expects a record ID string and searches for the cursor row in the current result set.

## Investigation approach

Trace one page boundary through a tied timestamp, a duplicated identifier, and a deleted boundary row. A robust cursor must encode the complete stable ordering key so the next-page rule does not require finding the old row.

## Correction

The solution validates a positive non-boolean limit and a `(created_at, id)` cursor, filters malformed records, resolves duplicate IDs to the highest version, and sorts by both timestamp and ID. It then selects records strictly greater than the cursor key. A cursor therefore remains usable when its row disappears.

## Regression tests

Tests cover tied timestamps, next-page continuation, deleted cursor rows, duplicate versions, malformed records, empty results, and invalid limits/cursors. Equal-version duplicates retain the first source row, making that conflict rule explicit.
