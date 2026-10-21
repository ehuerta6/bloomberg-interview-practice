# Ticket #15 — Session Revocation

**Difficulty:** Easy

## Problem

### Reported symptom

A user logs out, but the same session token still opens protected pages; logging out on one device must not sign out all devices.

### Scenario

A user has active sessions on a phone and laptop. Logout revokes one session, and repeated logout requests may arrive from a browser retry.

## Acceptance Criteria
- A revoked session is no longer authorized for protected access.
- Revocation is scoped to one session, persisted, and idempotent; another device’s session remains active.
- Invalid requests must leave persisted state unchanged.

## State Invariants

Revocation is scoped to one session, persisted, and idempotent; another device’s session remains active.

## Investigation

Trace the stored session state and the authorization check. Compare access before logout, after logout, and after a repeated logout call. Add regression coverage for the behavior you reproduce.

## Starter Code

[View starter code](../../round-2/15-session-revocation/)

## Reference Solution

[View solution](../../solutions/round-2/15-session-revocation/)
