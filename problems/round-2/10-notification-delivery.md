# Ticket #10 — Notification Delivery

**Difficulty:** Medium

## Context

You maintain notifications for completed reports. An event ID identifies one
recipient/message pair. The producer may resend that event after an uncertain
response. Deduplication means that replaying a successfully sent event must not
contact the provider again. The supplied recording provider is an in-memory fake.

## Practice report

With a provider that succeeds, call
`deliver("evt-1", "riley", "Your report is ready")` twice.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Provider calls | 2 | 1 |
| Stored attempt count for `evt-1` | 2 | 1 |
| Stored delivery status | `sent` | `sent` |

A single stored row is insufficient evidence of one send; inspect provider
calls as well as delivery records.

## Acceptance Criteria

- An exact replay after success returns the sent record without another send
  or attempt. Reusing an event ID for a different recipient or message raises
  `ValueError` without changing the original delivery or calling the provider.
- Persist the delivery's incremented attempt count and sending state before
  each provider call, then persist its outcome.
- With the default limit of 3, outcomes `[False, False, True]` end in `sent`
  after 3 attempts. Three failures leave a persisted `failed` record.
- `retry(event_id)` may resume a failed record with another bounded set of
  attempts; attempt history accumulates. A successful later attempt can move
  it to `sent`.
- Retrying a sent record has no additional effect. Retrying an unknown event
  raises `KeyError` without creating a record.

## Out of Scope

Use the included store and provider fake. Real email/SMS services, backoff
scheduling, crash recovery across processes, and new payload-validation rules
are outside this ticket.

## Investigation

Trace submission and operator retry through the delivery store and provider.
Add assertions for persisted attempts, status, and provider calls on success,
replay, transient failure, and exhausted retries. Keep request identity and
side effects consistent across those paths.

## Starter Code

[View starter code](../../round-2/10-notification-delivery/)

## Reference Solution

[View solution](../../solutions/round-2/10-notification-delivery/)
