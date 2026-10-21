# PR #02 — Event Scheduler

**Difficulty:** Medium

**PR title:** Check event availability

## Summary

This change adds an availability check for a new event against a collection of scheduled events.

## Expected behavior
- Each event is represented by a start and end time and covers the half-open interval `[start, end)`.
- Adjacent events are allowed; an event ending at time `12` does not conflict with one starting at `12`.
- Any actual overlap is rejected.
- An interval with `start >= end` is invalid and rejected.
- Checking availability does not modify the existing event collection.

## Review task

Review the implementation and tests against these rules. Correct the implementation and any tests that do not accurately express the expected behavior. Add regression cases where the current suite is insufficient.

## Starter Code

[View starter code](../../round-1/02-event-scheduler/)

## Reference Solution

[View solution](../../solutions/round-1/02-event-scheduler/)
