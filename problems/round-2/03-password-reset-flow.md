# Ticket #03 — Password Reset Flow

**Difficulty:** Medium

## Problem

### Reported symptom

A customer who requests a second password reset can still use the older email link to change the password.

### Scenario

A user requests a reset, waits for a message, then requests another after not receiving the first. The user reports that both links still work, including a link that has passed its stated lifetime.

## Acceptance Criteria
- Reset links have a fixed expiration time.
- A token can successfully change a password only once.
- Requesting a newer reset invalidates older outstanding tokens for the same user.
- Unknown, expired, used, or invalidated tokens leave the stored password unchanged.
- Token expiry can be tested deterministically without waiting.

## State Invariants
- At most one outstanding reset token per user is usable.
- A rejected reset attempt never changes the password.
- A token’s successful use is a one-way state transition.

## Investigation

Trace token creation, storage, and password changes. Use a controllable clock to compare the exact expiry boundary, then test retries and state after rejected requests. Check that the tests assert persisted password state.

## Starter Code

[View starter code](../../round-2/03-password-reset-flow/)

## Reference Solution

[View solution](../../solutions/round-2/03-password-reset-flow/)
