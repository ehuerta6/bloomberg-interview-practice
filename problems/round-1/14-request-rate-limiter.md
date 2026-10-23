# PR #14 — Request Rate Limiter

**Difficulty:** Hard

**PR title:** Enforce per-user request limits over a sliding window

## Summary

An API gateway gives each user a limited number of accepted requests during a recent time interval. One user's traffic must not spend another user's allowance, and a rejected request must not delay the next available slot. You are reviewing a limiter that receives numeric timestamps from its caller, making the admission decisions repeatable.

## Input and output

`RequestRateLimiter(limit, window_seconds)` creates a limiter. `allow(user_id, timestamp)` returns whether the request is accepted. The limit is a positive integer and the window is a positive finite duration.

## Expected behavior and invariants
- Track requests independently for each nonblank user ID.
- For a request at time `t`, the active interval is `(t - window_seconds, t]`. A request exactly at the left cutoff has expired.
- Accept a request only when fewer than `limit` accepted requests for that user remain in the active interval.
- Rejected attempts do not consume a slot or extend the window.
- Per-user timestamps must be finite and nondecreasing. Invalid configuration or request input raises `ValueError`.

## Contract example

For `limiter = RequestRateLimiter(limit=2, window_seconds=10)`, process these calls in order:

| User | Timestamp | Expected `allow` result |
| --- | ---: | --- |
| `"a"` | 0 | `True` |
| `"a"` | 1 | `True` |
| `"b"` | 2 | `True` |
| `"a"` | 2 | `False` |
| `"a"` | 10 | `True` |

At time 10, user a's request at time 0 is outside `(0, 10]`, while the accepted request at time 1 remains active. The rejected attempt at time 2 does not use a slot.

## Review task

Review the admission results and test assertions against each user's accepted-request history. Correct discrepancies and add deterministic sequences for the exact cutoff, repeated rejections, and invalid or decreasing timestamps. Explain how the tests show both independent user allowances and the time when an allowance becomes available again.

## Starter Code

[View starter code](../../round-1/14-request-rate-limiter/)

## Reference Solution

[View solution](../../solutions/round-1/14-request-rate-limiter/)
