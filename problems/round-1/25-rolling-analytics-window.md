# PR #25 — Rolling Analytics Window

**Difficulty:** Medium

## PR title

Sum events inside a rolling window

## Summary

An analytics endpoint reports a metric over a trailing duration. Review whether interval endpoints, future events, and malformed inputs are handled consistently.

## Input and output

`rolling_total(events, now, window_seconds)` accepts event dictionaries with an ISO 8601 `timestamp` and numeric `value`, a reference `datetime`, and a nonnegative window duration in seconds. It returns the sum of included event values.

## Expected behavior, edge cases, and invariants
- Include timestamps in the closed interval `[now - window, now]`; exclude older and future events.
- Count negative event values as supplied. An empty window sums to zero.
- Reject invalid timestamps or event values and negative, boolean, or nonnumeric window lengths with `ValueError`.
- Event timestamps and `now` must both be timezone-aware or both naive.

## Review task

Test events at both endpoints and just outside the interval. Include negative values, zero-length windows, malformed values, and timezone mismatches.


## Starter Code

[View starter code](../../round-1/25-rolling-analytics-window/)

## Reference Solution

[View solution](../../solutions/round-1/25-rolling-analytics-window/)
