# Course Enrollment Reference Solution

## What Was Broken?

A learner could enroll in a course without completing its prerequisite.

## Reproduce the Behavior

From this folder, run `python3 test_enrollment.py`; `test_prerequisite_is_required_before_enrollment` tries to enroll `s1` in `advanced` before `intro` is marked complete. The starter creates an enrollment row rather than rejecting the request.

## Investigation

Trace prerequisite evaluation and capacity checks before the enrollment row is written. Then inspect enrollment statuses for a full course: after a current learner drops, determine which waitlisted learner is promoted and whether a repeated drop changes the roster again.

## Fix

The service verifies all prerequisites before creating an enrollment. Capacity counts only enrolled rows, waitlisted rows remain separate, and dropping an enrolled row promotes one waiting learner.

## Regression Tests

The tests cover completed and missing prerequisites, enrollment at capacity, waitlist ordering, drop-and-promote behavior, duplicate enrollment, and invalid course or learner IDs. Assertions check both the result and persisted statuses so capacity counts only enrolled students.

## Run the Corrected Tests

```sh
python3 test_enrollment.py
```
