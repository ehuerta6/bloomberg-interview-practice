# Ticket #10 — Notification Delivery

**Difficulty:** Medium

## Problem

### Reported symptom

The same event appears twice in a recipient’s inbox, while a temporary provider outage leaves some messages in an ambiguous state.

### Scenario

An event producer retries after a timeout. Delivery attempts can fail transiently, and a later operator retry should resume a failed delivery without sending an already-confirmed notification again.

## Acceptance Criteria
- A notification is keyed by event ID; repeated submissions of the same event do not produce another send after success.
- A delivery record is persisted before the external send attempt and records each attempt and terminal state.
- Invalid requests must leave persisted state unchanged.

## State Invariants

A delivery record is persisted before the external send attempt and records each attempt and terminal state.

## Investigation

Trace event submission, persistence, provider calls, and operator retry. Determine which record state should survive a retry and prove both transient and exhausted failure behavior. Add regression coverage for the behavior you reproduce.

## Starter Code

[View starter code](../../round-2/10-notification-delivery/)

## Reference Solution

[View solution](../../solutions/round-2/10-notification-delivery/)
