# Appointment Rescheduling Reference Solution

## What Was Broken?

A conflicting reschedule returned failure after leaving the appointment at the requested time.

## Reproduce the Behavior

From this folder, run `python3 test_rescheduling.py`; `test_conflict_leaves_original_appointment_unchanged` moves `a1` from `10:00` to `11:00`, which is occupied by `a2`. The starter reports a conflict but leaves `a1` at the new time, creating a double booking and losing the original slot.

## Investigation

Capture all appointment times before requesting an occupied slot. Trace when the original slot is released and ensure a failed request restores the exact prior schedule. The tests check the stored records and state totals so the failure is visible at the domain boundary.

## Fix

The service records the old time, applies the candidate move, checks for another appointment at that time, and restores the old time on conflict. Ownership is checked before the schedule can change.

## Regression Tests

The corrected suite covers the reported failure, normal success, rejected and repeated requests, and state invariants. It also checks boundary or retry behavior with deterministic clocks and in-memory repositories. All assertions inspect returned results and persisted state.

## Run the Corrected Tests

```sh
python3 test_rescheduling.py
```
