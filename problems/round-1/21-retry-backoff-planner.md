# PR #21 — Retry Backoff Planner

**Difficulty:** Medium

## PR title

Validate and cap retry delays

## Summary

A client library plans waits between attempts after temporary failures. Review whether the schedule respects its retry count, multiplier, and configured ceiling.

## Input and output

`retry_delays(max_retries, base_delay, multiplier=2, max_delay=None)` returns a list with one wait duration per retry after the initial request.

`max_retries` is a nonnegative integer. Delay settings must be numeric and nonnegative, and `multiplier` must be at least 1. Booleans are not accepted as integers or numeric settings.

## Expected behavior, edge cases, and invariants
- The first wait equals `base_delay`; each later wait is the previous wait multiplied by `multiplier`.
- When supplied, `max_delay` caps every wait, including the first.
- A zero retry count returns an empty list.
- Invalid retry counts or delay settings raise `ValueError`.

## Review task

Trace the schedule before and after the cap engages. Check fractional inputs, zero retries, the cap below the base delay, and invalid booleans or negative values.


## Starter Code

[View starter code](../../round-1/21-retry-backoff-planner/)

## Reference Solution

[View solution](../../solutions/round-1/21-retry-backoff-planner/)
