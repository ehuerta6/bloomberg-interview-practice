# PR #14 — Request Rate Limiter

**Difficulty:** Hard

**PR title:** Enforce per-user request limits over a sliding window

## Summary

An API gateway needs to allow a bounded number of requests per user over a rolling interval. Review state isolation, timestamp ordering, and the exact window boundary.

## Input and output

`RequestRateLimiter(limit, window_seconds)` creates a limiter. `allow(user_id, timestamp)` returns whether the request is accepted. The limit is a positive integer and the window is a positive finite duration.

## Expected behavior and invariants
- Track requests independently for each nonblank user ID.
- For a request at time `t`, the active interval is `(t - window_seconds, t]`. A request exactly at the left cutoff has expired.
- Accept a request only when fewer than `limit` accepted requests for that user remain in the active interval.
- Rejected attempts do not consume a slot or extend the window.
- Per-user timestamps must be finite and nondecreasing. Invalid configuration or request input raises `ValueError`.

## Review task

Interleave requests from two users and trace the active timestamps at each call. Exercise requests just before, exactly at, and just after the cutoff, including a rejected request between accepted ones.

## Starter Code

[View starter code](../../round-1/14-request-rate-limiter/)

## Reference Solution

[View solution](../../solutions/round-1/14-request-rate-limiter/)
