# Ticket #25 — Webhook Event Processing

**Difficulty:** Medium

## Problem

### Reported symptom

A delivery partner retries webhook notifications and occasionally sends old notifications after newer ones. The order timeline must remain monotonic, and retries must not repeat state effects.

### Scenario

Deliver events in order, then replay one and send a delayed lower sequence. Inspect current status, processed IDs, and history. Also try a conflicting event with the same sequence and a new ID.

## Acceptance Criteria
- Apply a known event only once by event ID.
- Never let a stale or same-sequence event regress order state.
- Record stale event IDs so their retries remain duplicates.
- Reject malformed events and unknown orders without changing order state.
- Keep history for applied events in increasing sequence order.

## State Invariants
- For each order, current status matches the highest applied sequence.
- An event ID produces at most one state effect.
- History is strictly increasing by sequence.
- Invalid events have no side effects.

## Investigation

Deliver increasing event sequences, replay an already-seen event ID, then send a delayed lower sequence and a different event at the current sequence. Verify order status and history remain monotonic and that malformed or unknown-order events have no effects.

## Starter Code

[View starter code](../../round-2/25-webhook-event-processing/)

## Reference Solution

[View solution](../../solutions/round-2/25-webhook-event-processing/)
