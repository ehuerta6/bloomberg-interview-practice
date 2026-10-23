# Ticket #25 — Webhook Event Processing

**Difficulty:** Medium

## Context

You maintain an order-status receiver for a delivery partner. A **webhook** is
an incoming event notification; partners may retry it or deliver it late.
Event IDs identify notifications globally. A sequence number orders updates
within one order; monotonic history means applied sequence numbers only increase.

## Practice report

Create order `o1`. Deliver event `e2` at sequence 2 with status `shipped`, then
a different event `e1` at sequence 1 with status `paid`.

| Observation after the delayed event | Current starter | Expected |
| --- | --- | --- |
| Result for `e1` | `applied` | `stale` |
| Current order status | `paid` | `shipped` |
| Applied-history sequences | `[2, 1]` | `[2]` |

Both IDs must be remembered as processed, so retrying the stale notification
returns `duplicate` without another state effect.

## Acceptance Criteria

- Validate nonempty event/order IDs, an integer sequence of at least 1 excluding
  booleans, and a supported status: `created`, `paid`, `shipped`, `delivered`, or
  `cancelled`. Malformed events are rejected without side effects. A new valid
  event ID for an unknown order is also rejected without side effects.
- Apply a valid event ID at most once globally, including across different
  orders. A well-formed request using a processed ID returns `duplicate` without
  changing state.
- For each order, apply only sequences strictly greater than its latest applied
  sequence. A new ID at a lower or equal sequence returns `stale`, preserving
  current status and history while remembering that ID as processed.
- Applied events update status and append `(sequence, event_id, status)` to
  history. History is strictly increasing and status matches its highest sequence.
- Different orders have independent sequence histories. Sequence ordering does
  not imply a new business rule restricting transitions between supported statuses.

## Out of Scope

Keep the supplied route and repository. Partner authentication, network delivery,
message queues, and a new order-status transition graph are outside this ticket.

## Investigation

Reproduce the delayed event, then test equal sequences under different IDs,
exact retries, independent orders, and malformed requests. Assert status,
applied history, and remembered IDs after each call, including a stale-event retry.

## Starter Code

[View starter code](../../round-2/25-webhook-event-processing/)

## Reference Solution

[View solution](../../solutions/round-2/25-webhook-event-processing/)
