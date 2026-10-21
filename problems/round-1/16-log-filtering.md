# PR #16 — Log Filtering

**Difficulty:** Easy

**PR title:** Filter structured logs by severity and time range

## Summary

A log viewer needs to filter structured entries by a minimum severity and optional timestamp bounds. Review severity ordering, boundary inclusion, and resilience to malformed records.

## Input and output

`filter_logs(entries, minimum_severity="INFO", start_time=None, end_time=None)` accepts a list of entries with numeric `timestamp` and a `severity`. It returns valid matching entries in their input order.

## Expected behavior and invariants
- Severity levels, from lowest to highest, are DEBUG, INFO, WARNING, ERROR, and CRITICAL. Matching severity names are case-insensitive.
- Return entries at or above the requested minimum severity.
- Optional start and end timestamps are inclusive. Either bound may be omitted; if both are supplied, start must not exceed end.
- Ignore malformed entries, including missing fields, non-finite or nonnumeric timestamps, and unknown severity names.
- Reject invalid filter arguments with `ValueError` and preserve the order of the valid matching entries.

## Review task

Build a few entries at each severity and exactly on both time bounds. Add malformed entries to the same list and confirm filtering continues while the valid results stay ordered.

## Starter Code

[View starter code](../../round-1/16-log-filtering/)

## Reference Solution

[View solution](../../solutions/round-1/16-log-filtering/)
