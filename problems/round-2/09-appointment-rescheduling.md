# Ticket #09 — Appointment Rescheduling

**Difficulty:** Medium

## Context

You maintain a clinic's appointment tool. Each string time slot can hold one
appointment. A patient may reschedule only their own appointment; a failed move
must preserve the original booking so the patient still has a confirmed time.

## Practice report

Store appointment `a1` for `patient-a` at `10:00` and `a2` for `patient-b` at
`11:00`. Call `reschedule("a1", "patient-a", "11:00")`.

| Observation after the request | Current starter | Expected |
| --- | --- | --- |
| Result | `"conflict"` | `"conflict"` |
| `a1` time | `11:00` | `10:00` |
| `a2` time | `11:00` | `11:00` |

The rejection must preserve the complete schedule, including the patient's
original slot and the other patient's appointment.

## Acceptance Criteria

- Only an appointment's owner may move it. Unknown appointments, a different
  patient, or an empty requested time return `not_found` without schedule changes.
- A time occupied by another appointment returns `conflict` and leaves every
  appointment unchanged.
- A successful move returns `rescheduled`, frees the old slot, and places the
  appointment in exactly one new slot.
- Moving to the current slot succeeds without creating a duplicate.
- If a patient has already moved successfully, a later rejected move preserves
  that current booking, not an earlier time.

## Out of Scope

Use the supplied slot strings and in-memory repository. Calendar parsing,
time zones, appointment duration, reminders, and clinical records are outside
this ticket.

## Investigation

Trace ownership, conflict handling, and persisted appointment state for the
report. Add tests for a free slot, the current slot, a conflict, and a conflict
after a successful move. Compare the full schedule before and after failures.

## Starter Code

[View starter code](../../round-2/09-appointment-rescheduling/)

## Reference Solution

[View solution](../../solutions/round-2/09-appointment-rescheduling/)
