# PR #16 — Log Filtering

**Difficulty:** Easy

**PR title:** Filter structured logs by severity and time range

## Summary

An operator uses a log viewer to inspect messages at a chosen severity within a time range. The stored list may also contain malformed records; those records should not prevent the operator from seeing valid matching entries. You are reviewing the filtering PR and its interpretation of the selected boundaries.

## Input and output

`filter_logs(entries, minimum_severity="INFO", start_time=None, end_time=None)` accepts a list of entries with numeric `timestamp` and a `severity`. It returns valid matching entries in their input order.

## Expected behavior and invariants
- Severity levels, from lowest to highest, are DEBUG, INFO, WARNING, ERROR, and CRITICAL. Matching severity names are case-insensitive.
- Return entries at or above the requested minimum severity.
- Optional start and end timestamps are inclusive. Either bound may be omitted; if both are supplied, start must not exceed end.
- Ignore malformed entries, including missing fields, non-finite or nonnumeric timestamps, and unknown severity names.
- Reject invalid filter arguments with `ValueError` and preserve the order of the valid matching entries.

## Contract example

Input entries:

```python
[
    {"timestamp": 1, "severity": "DEBUG", "message": "start"},
    {"timestamp": 2, "severity": "INFO", "message": "ready"},
    {"timestamp": 3, "severity": "WARNING", "message": "slow"},
    {"timestamp": 4, "severity": "ERROR", "message": "failed"},
]
```

With minimum severity `"INFO"`, `start_time=2`, and `end_time=3`, return the original `ready` entry followed by the original `slow` entry. Both endpoints belong to the range. Appending `{"message": "missing fields"}` to this input must leave that result unchanged. An unknown minimum severity such as `"TRACE"` is an invalid filter and raises `ValueError`.

## Review task

Review the filter and assertions against severity order, inclusive time bounds, and the distinction between a bad record and a bad filter. Correct discrepancies and add cases with mixed valid and malformed entries, omitted bounds, and entries exactly on each supplied bound. Check the returned entries and their order.

## Starter Code

[View starter code](../../round-1/16-log-filtering/)

## Reference Solution

[View solution](../../solutions/round-1/16-log-filtering/)
