# Ticket #01 — Event Registration

**Difficulty:** Medium

## Problem

### Reported symptom

After a student cancels an event registration, another student may still be told that the event is full. Investigate the request path and determine why a cancelled registration continues to affect capacity.

### Relevant scenario

An event has a fixed capacity. Several students register, one registration is cancelled, and a new student tries to take the released place. Requests pass through route, service, repository, and model code.

## Acceptance Criteria
- Active registrations consume capacity; cancelled registrations do not.
- A student cannot hold duplicate active registrations for the same event.
- Capacity is never exceeded, and cancelling an active registration frees its place.
- Invalid or repeated cancellation attempts do not damage registration state.

## State Invariants
- Each registration has one status, and only active registrations count toward capacity.
- Rejected requests leave the stored registrations unchanged.

## Investigation

Trace registration creation and cancellation through the route, service, repository, and data model. Compare behavior with the tests and decide which assertions prove the capacity and state invariants. Make a focused fix and add regression coverage for the behavior you reproduce.

## Starter Code

[View starter code](../../round-2/01-event-registration/)

## Reference Solution

[View solution](../../solutions/round-2/01-event-registration/)
