# PR #05 — Session Token Expiration

**Difficulty:** Medium

**PR title:** Track issued and revoked session tokens

## Summary

The authentication service now keeps an in-memory registry of session tokens so request handling can reject expired or revoked credentials. The clock is passed in by the caller to make checks deterministic.

## Expected behavior
- `issue(token_id, issued_at, expires_at)` accepts a new nonblank ID only when both timestamps are timezone-aware and expiration follows issue time. Duplicate IDs are rejected.
- A token is valid only when it exists, has not been revoked, and `issued_at <= now < expires_at`.
- Revoking an issued token makes it invalid immediately. Revoking an unknown token returns false and does not create registry state.
- Time checks use the supplied `now`; they must not depend on the machine's wall clock.

## Review task

Review the registry's state transitions and the validity interval. Test the instant before issue, the issue instant, and the exact expiration instant. Check whether revocation and duplicate IDs behave consistently without relying on the current time.

## Starter Code

[View starter code](../../round-1/05-session-token-expiration/)

## Reference Solution

[View solution](../../solutions/round-1/05-session-token-expiration/)
