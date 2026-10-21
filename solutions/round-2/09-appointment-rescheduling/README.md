# Appointment Rescheduling Reference Solution

## What Was Broken?

A conflicting reschedule returned failure after leaving the appointment at the requested time.

## Reproduce the Behavior

From this folder, run `python3 test_rescheduling.py`; `test_conflict_leaves_original_appointment_unchanged` moves `a1` from `10:00` to `11:00`, which is occupied by `a2`. The starter reports a conflict but leaves `a1` at the new time, creating a double booking and losing the original slot.

## Investigation

Capture the schedule before requesting a slot that belongs to another appointment. Trace the order of ownership validation, conflict detection, slot release, and persistence. After a rejected move, compare the full schedule with the original state and check that a valid later reschedule still works.

## Fix

The service records the old time, applies the candidate move, checks for another appointment at that time, and restores the old time on conflict. Ownership is checked before the schedule can change.

## Regression Tests

The tests cover a successful move, an occupied-slot conflict with exact rollback, an unknown appointment, a caller who does not own the appointment, and a request for the current slot. They assert that failures preserve the original time and never leave two appointments at the same slot.

## Run the Corrected Tests

```sh
python3 test_rescheduling.py
```
