# Ticket #03 — Password Reset Flow

**Difficulty:** Medium

## Context

You maintain account recovery for a member portal. A reset token is the ID in a
password-reset link. Each token has an expiration time and may change a password
once. The service receives a clock, so tests can choose the time directly.

## Practice report

At 12:00 on 2030-01-01, issue token `first` for `u1`, then issue `second` for the
same user before either token is used. Call `reset("first", "old-path")`.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Reset result | `True` | `False` |
| Stored password hash for `u1`, initially absent | `"old-path"` | Still absent |

The newer token should remain usable after the rejected attempt with `first`.

## Acceptance Criteria

- Issued tokens have a fixed lifetime (20 minutes by default). A token is valid
  before its expiration and invalid at the exact expiration instant and afterward.
- Issuing a newer token invalidates earlier unused tokens for that user without
  affecting tokens belonging to other users.
- A successful reset changes the stored password hash and consumes the token
  once. A repeated use cannot replace that password again.
- Unknown, expired, used, or invalidated tokens and an empty replacement hash
  leave the stored password unchanged. Invalid issuance or an existing token ID
  must not replace a token.
- Test time boundaries by controlling the supplied clock, without real waits.

## Out of Scope

Work with the supplied token IDs and password-hash strings. Email delivery,
password hashing, token generation, and a production authentication system are
outside this exercise.

## Investigation

Trace issuance and reset through the token repository and service. Prove the
old-link case, the usable newer link, single use, and the expiration boundary by
asserting both results and stored passwords. Keep the correction focused on
this lifecycle.

## Starter Code

[View starter code](../../round-2/03-password-reset-flow/)

## Reference Solution

[View solution](../../solutions/round-2/03-password-reset-flow/)
