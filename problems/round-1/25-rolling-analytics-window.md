# PR #25 — Rolling Analytics Window

**Difficulty:** Medium

## PR title

Sum events inside a rolling window

## Summary

An analytics page displays the total change in a metric during a recent interval. Corrections may have negative values, and events beyond the reference time must not contribute yet. You are reviewing the rolling-total PR so the endpoint uses a supplied time and an explicit duration rather than an assumed current clock.

## Input and output

`rolling_total(events, now, window_seconds)` accepts event dictionaries with an ISO 8601 `timestamp` and numeric `value`, a reference `datetime`, and a nonnegative window duration in seconds. It returns the sum of included event values.

## Expected behavior, edge cases, and invariants
- Include timestamps in the closed interval `[now - window, now]`; exclude older and future events.
- Count negative event values as supplied. An empty window sums to zero.
- Reject invalid timestamps or event values and negative, boolean, or nonnumeric window lengths with `ValueError`.
- Event timestamps and `now` must both be timezone-aware or both naive.

## Contract example

Let `now=datetime(2025, 1, 1, 12, 0, 0)` and `window_seconds=180`. Use these events in a list, with no timezone offsets:

| Timestamp | Value | Included? |
| --- | ---: | --- |
| `"2025-01-01T11:56:59"` | 7 | No |
| `"2025-01-01T11:57:00"` | 7 | Yes |
| `"2025-01-01T11:59:00"` | -3 | Yes |
| `"2025-01-01T12:00:00"` | 4 | Yes |
| `"2025-01-01T12:00:01"` | 9 | No |

The expected total is `8` (`7 - 3 + 4`). With the same input and `window_seconds=0`, only the event exactly at `now` is included, giving `4`. An empty input list returns `0`.

## Review task

Review the aggregation and assertions against both inclusive endpoints, future exclusion, and numeric values. Correct discrepancies and add cases for a zero-duration interval, malformed records, invalid window settings, and timezone mismatches. Explain how the tests verify the total and the required rejection behavior separately.

## Starter Code

[View starter code](../../round-1/25-rolling-analytics-window/)

## Reference Solution

[View solution](../../solutions/round-1/25-rolling-analytics-window/)
