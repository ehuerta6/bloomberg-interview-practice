# PR #21 — Retry Backoff Planner

**Difficulty:** Medium

## PR title

Validate and cap retry delays

## Summary

A client library waits before retrying a request after a temporary failure. Increasing waits reduce repeated traffic, while a configured ceiling limits how long the caller waits between attempts. You are reviewing the helper that plans these delays; the initial request itself has no wait entry in the returned list.

## Input and output

`retry_delays(max_retries, base_delay, multiplier=2, max_delay=None)` returns a list with one wait duration per retry after the initial request.

`max_retries` is a nonnegative integer. Delay settings must be numeric and nonnegative, and `multiplier` must be at least 1. Booleans are not accepted as integers or numeric settings.

## Expected behavior, edge cases, and invariants
- The first wait equals `base_delay`; each later wait is the previous wait multiplied by `multiplier`.
- When supplied, `max_delay` caps every wait, including the first.
- A zero retry count returns an empty list.
- Invalid retry counts or delay settings raise `ValueError`.

## Contract examples

All delay values use the same caller-chosen time unit, such as seconds.

| Call | Expected return |
| --- | --- |
| `retry_delays(4, 1)` | `[1, 2, 4, 8]` |
| `retry_delays(5, 2, max_delay=5)` | `[2, 4, 5, 5, 5]` |
| `retry_delays(3, 2, max_delay=1)` | `[1, 1, 1]` |
| `retry_delays(3, 0.25)` | `[0.25, 0.5, 1.0]` |
| `retry_delays(0, 1)` | `[]` |

`retry_delays(-1, 1)` and `retry_delays(3, 1, multiplier=0)` raise `ValueError`.

## Review task

Review the planner and tests against the number of retries, growth rule, and per-wait ceiling. Correct discrepancies and add assertions for fractional waits, a cap smaller than the base, zero retries, and invalid settings. Explain how the tests distinguish a valid empty plan from an invalid request.

## Starter Code

[View starter code](../../round-1/21-retry-backoff-planner/)

## Reference Solution

[View solution](../../solutions/round-1/21-retry-backoff-planner/)
