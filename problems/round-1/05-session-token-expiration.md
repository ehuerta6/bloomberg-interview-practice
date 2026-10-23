# PR #05 — Session Token Expiration

**Difficulty:** Medium

**PR title:** Track issued and revoked session tokens

## Summary

A signed-in user's request carries a token ID. The authentication service needs an in-memory `TokenRegistry` to decide whether that credential can be used at the request's supplied time. You are reviewing issuance, revocation, and validity checks; callers supply the clock so tests and request handling can use the same time.

## Expected behavior
- `issue(token_id, issued_at, expires_at)` accepts a new nonblank ID only when both timestamps are timezone-aware and expiration follows issue time. Duplicate IDs are rejected.
- A token is valid only when it exists, has not been revoked, and `issued_at <= now < expires_at`.
- Revoking an issued token makes it invalid immediately. Revoking an unknown token returns false and does not create registry state.
- Time checks use the supplied `now`; they must not depend on the machine's wall clock.

## Contract example

Issue `"s-1"` at `2030-01-01 00:00:00 UTC`, expiring at `01:00:00 UTC` on the same day. For this known, unrevoked token:

| Supplied `now` | Expected `is_valid("s-1", now)` |
| --- | --- |
| `2029-12-31 23:59:59 UTC` | `False` |
| `2030-01-01 00:00:00 UTC` | `True` |
| `2030-01-01 00:30:00 UTC` | `True` |
| `2030-01-01 01:00:00 UTC` | `False` |

After `revoke("s-1")` returns `True`, the token is invalid even at an otherwise valid time. Revoking `"missing"` returns `False` and adds no registry entry.

## Review task

Review the registry and tests against the validity interval and revocation rules. Add deterministic cases for the issue and expiration boundaries, repeated IDs, and rejected issuance. Explain which assertions check return values and which verify that rejected operations leave registry state intact.

## Starter Code

[View starter code](../../round-1/05-session-token-expiration/)

## Reference Solution

[View solution](../../solutions/round-1/05-session-token-expiration/)
