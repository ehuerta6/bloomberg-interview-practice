# Ticket #15 — Session Revocation

**Difficulty:** Easy

## Context

You maintain sessions for a member portal. Each login creates a separate
session ID for a device. Revocation ends that session's authorization while
retaining its record and first logout time. Logging out a phone must leave the
same user's laptop session usable.

## Practice report

Log in `alice` as `s-1` on a phone and `s-2` on a laptop. Call
`logout("s-1", "10:00")`, then check authorization for both IDs.

| Observation | Current starter | Expected |
| --- | --- | --- |
| `is_authorized("s-1")` | `True` | `False` |
| `is_authorized("s-2")` | `True` | `True` |
| Saved `s-1.revoked_at` | `"10:00"` | `"10:00"` |

## Acceptance Criteria

- An existing session is authorized before logout and unauthorized afterward.
  Unknown session IDs are never authorized.
- Logout affects only the requested session and persists its first revocation
  time. A repeated logout succeeds without replacing that time or affecting
  another device.
- Logging out an unknown session returns `False` and creates no record.
- A duplicate login session ID raises `ValueError` without replacing the
  original user or device.

## Out of Scope

Use the supplied session IDs and stored time strings. Session expiry, password
checks, token cryptography, and a logout-all-devices feature are outside this ticket.

## Investigation

Trace login, logout, stored state, and authorization for the two-device report.
Add assertions before logout, after logout, and after a repeated logout with a
later time. Verify both devices and the original saved revocation time.

## Starter Code

[View starter code](../../round-2/15-session-revocation/)

## Reference Solution

[View solution](../../solutions/round-2/15-session-revocation/)
