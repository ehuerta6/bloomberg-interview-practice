# Course Enrollment Reference Solution

## What Was Broken?

A learner could enroll in a course without completing its prerequisite.

## Reproduce the Behavior

From this folder, run `python3 test_enrollment.py`; `test_prerequisite_is_required_before_enrollment` tries to enroll `s1` in `advanced` before `intro` is marked complete. The starter creates an enrollment row rather than rejecting the request.

## Investigation

Follow prerequisite evaluation before enrollment creation, then inspect counts by state. Drop a learner from a full course and verify that exactly one eligible waitlisted row is promoted. The tests check the stored records and state totals so the failure is visible at the domain boundary.

## Fix

The service verifies all prerequisites before creating an enrollment. Capacity counts only enrolled rows, waitlisted rows remain separate, and dropping an enrolled row promotes one waiting learner.

## Regression Tests

The corrected suite covers the reported failure, normal success, rejected and repeated requests, and state invariants. It also checks boundary or retry behavior with deterministic clocks and in-memory repositories. All assertions inspect returned results and persisted state.

## Run the Corrected Tests

```sh
python3 test_enrollment.py
```
