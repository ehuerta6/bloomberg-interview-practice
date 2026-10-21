# Ticket #08 — Course Enrollment

**Difficulty:** Medium

## Problem

### Reported symptom

A learner can enter an advanced course without completing its prerequisite.

### Scenario

Courses have prerequisites and limited seats. When a course is full, additional eligible learners wait in order; a dropped seat should be offered to the next learner.

## Acceptance Criteria
- A learner must complete every prerequisite before joining a course or its waitlist.
- Enrolled learners never exceed course capacity.
- Eligible learners join the waitlist when no seat is available.
- Waitlisted learners do not consume enrolled capacity.
- A learner cannot create duplicate active enrollment or waitlist entries.
- Dropping an active enrollment promotes the next waitlisted learner once.

## State Invariants
- Only completed courses satisfy prerequisites.
- Each learner has at most one active row per course.
- Waitlist promotion preserves capacity and does not promote the same row twice.

## Investigation

Trace prerequisite checks and enrollment states through a full-course scenario. Compare active enrollment counts with waitlisted rows before and after a drop, and verify student and course state after rejected requests.

## Starter Code

[View starter code](../../round-2/08-course-enrollment/)

## Reference Solution

[View solution](../../solutions/round-2/08-course-enrollment/)
