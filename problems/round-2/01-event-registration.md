# Ticket #01 — Event Registration

**Difficulty:** Medium

## Context

You maintain registration for a campus career night. An event has a fixed number
of places. A registration links one student to one event; `active` registrations
use places, while `cancelled` records remain as history.

## Practice report

Create `career-night` with capacity 1. Through `post_registration`, register
student `s1` as `r1`, cancel `r1` through `delete_registration`, then submit
student `s2` as `r2` for the same event.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Result of the final registration request | Status 409 | Status 201 |
| Who occupies the single place afterward | Nobody; `r1` is cancelled | `s2`; `r1` stays cancelled |

These status values come from the supplied route adapter; no web server is
needed to reproduce the report.

## Acceptance Criteria

- Active registrations alone consume capacity, and their count never exceeds
  the event's capacity. Cancelling one active registration frees one place.
- A student cannot have two active registrations for the same event. A student
  whose earlier registration was cancelled can register again with a new ID.
- A registration ID cannot replace an existing record. Missing required request
  fields or an unknown event are rejected without creating a registration.
- Cancellation succeeds only for an existing active registration. An unknown or
  repeated cancellation leaves every stored registration unchanged.
- Every rejected registration leaves the stored registrations unchanged.

## Out of Scope

Keep the in-memory repository and route response shape. Event scheduling,
payments, waitlists, and concurrent database transactions are outside this ticket.

## Investigation

Reproduce the cancellation sequence through the route adapter and follow the
request through service, repository, and model code. Add focused regression
assertions for returned statuses and stored registration state; explain how they
prove that one place is released and cannot be occupied twice.

## Starter Code

[View starter code](../../round-2/01-event-registration/)

## Reference Solution

[View solution](../../solutions/round-2/01-event-registration/)
