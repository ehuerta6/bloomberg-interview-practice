# Ticket #09 — Appointment Rescheduling

**Difficulty:** Medium

## Problem

### Reported symptom

A patient trying to move an appointment into an occupied time can lose the original appointment.

### Scenario

A clinic has one appointment per time slot. Patients may reschedule only their own appointment, and a requested slot may have been taken already.

## Acceptance Criteria
- Only the appointment owner can request a change.
- A time already occupied by another appointment is rejected.
- A rejected reschedule preserves the original appointment and all other appointments.
- A successful reschedule frees the old slot and occupies the new slot.
- Unknown appointment identifiers do not change the schedule.
- Rescheduling to the same slot succeeds without creating a duplicate.

## State Invariants
- Every appointment occupies exactly one time slot.
- A failed operation leaves the full schedule unchanged.
- Ownership and conflict checks do not expose or alter another patient’s appointment.

## Investigation

Capture the schedule before a conflicting request and compare every appointment afterward. Trace the order of writes and checks, then inspect whether the tests prove ownership and rollback behavior.

## Starter Code

[View starter code](../../round-2/09-appointment-rescheduling/)

## Reference Solution

[View solution](../../solutions/round-2/09-appointment-rescheduling/)
