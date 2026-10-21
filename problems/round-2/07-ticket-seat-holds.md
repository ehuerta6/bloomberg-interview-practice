# Ticket #07 — Ticket Seat Holds

**Difficulty:** Medium

## Problem

### Reported symptom

A seat remains unavailable to other buyers after its hold time has passed.

### Scenario

Buyers temporarily hold individual seats while they complete checkout. Holds expire after a short interval; a successful buyer can confirm an active hold.

## Acceptance Criteria
- A seat has at most one active hold.
- An expired hold no longer blocks a new buyer.
- A hold identifier cannot be used to claim a second seat while its first hold is active.
- Only the owning buyer can confirm an unexpired hold.
- A confirmed seat remains unavailable to other buyers.
- Expiry behavior can be tested with a controllable clock.

## State Invariants
- No two active holds reserve the same seat.
- Rejected hold or confirmation attempts leave existing ownership unchanged.
- Confirmed holds do not expire through the temporary hold timeout.

## Investigation

Use a fixed clock to inspect the exact expiration boundary. Try a competing buyer, an expired hold, and reuse of a hold identifier while comparing both seats and hold ownership.

## Starter Code

[View starter code](../../round-2/07-ticket-seat-holds/)

## Reference Solution

[View solution](../../solutions/round-2/07-ticket-seat-holds/)
