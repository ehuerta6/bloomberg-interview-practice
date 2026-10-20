# Ticket 25: Webhook Event Processing (Medium)

## Ticket

Webhook Event Processing needs reliable state transitions.

## Reported symptom

A delivery partner retries webhook notifications and occasionally sends old notifications after newer ones. The order timeline must remain monotonic, and retries must not repeat state effects.

## Scenario

Deliver events in order, then replay one and send a delayed lower sequence. Inspect current status, processed IDs, and history. Also try a conflicting event with the same sequence and a new ID.

## Acceptance criteria

- Apply a known event only once by event ID.
- Never let a stale or same-sequence event regress order state.
- Record stale event IDs so their retries remain duplicates.
- Reject malformed events and unknown orders without changing order state.
- Keep history for applied events in increasing sequence order.

## State invariants

- For each order, current status matches the highest applied sequence.
- An event ID produces at most one state effect.
- History is strictly increasing by sequence.
- Invalid events have no side effects.

## Investigation task

Trace a normal operation, a boundary or failure case, and a repeated request across the route, service, and repository. Explain which state should change, which state must remain untouched, and how your regression tests demonstrate both outcomes. Keep the implementation in memory; no external services or frameworks are required.

## Run the starter tests

```sh
python3 test_webhook_events.py
```

## Exercise folders

- [Starter exercise](../../round-2/25-webhook-event-processing/)
- [Reference solution](../../solutions/round-2/25-webhook-event-processing/)
