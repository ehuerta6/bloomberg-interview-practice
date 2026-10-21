# Retry Backoff Planner — Reference Solution

## What broke

The draft passes `max_retries` directly to `range`, so `-1` silently produces an empty plan. It also accepts `multiplier=0`; for three retries and a base delay of 1, it returns `[1, 0, 0]` instead of rejecting a shrinking schedule.

## Reproduce the issue

From `round-1/21-retry-backoff-planner/`, run `python3 retry_plan.py`. `test_negative_retry_count_is_rejected` and `test_invalid_multiplier_is_rejected` fail because neither call raises `ValueError`. Run it in this solution folder to confirm the corrections.

## Investigation approach

Trace `retry_delays` through its `range(max_retries)` loop and the multiplier update. A negative count skips the loop entirely, while a zero multiplier erases later waits. Then inspect where `max_delay` is applied: the starter caps the completed list, which yields the same visible values for ordinary finite inputs but does not validate the schedule parameters.

## Correction

The solution validates that the retry count is a nonnegative non-boolean integer and that delay settings are numeric, non-boolean, and within range (`multiplier >= 1`). It caps each delay before appending it, then multiplies that capped wait to form the next candidate. This keeps every result at or below the ceiling and handles a cap smaller than the base delay.

## Regression tests

`test_negative_retry_count_is_rejected` and `test_invalid_multiplier_is_rejected` cover the starter defects. The suite also verifies exponential growth, a custom multiplier, fractional waits, zero retries, and both cap behavior and preservation of earlier waits. The solution adds `test_retry_count_must_not_be_boolean`. Run it with `python3 retry_plan.py`.
