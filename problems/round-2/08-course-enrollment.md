# Ticket #08 — Course Enrollment

**Difficulty:** Medium

## Context

You maintain course enrollment for a learning portal. A prerequisite is a course
the learner must have **completed**, not merely enrolled in. Enrolled learners
use seats; waitlisted learners are eligible learners waiting for a seat to open.

## Practice report

Add `intro` with capacity 2 and `advanced` with capacity 1 and prerequisite
`intro`. Learner `s1` has no completions. Call
`enroll("s1", "advanced", "e1")`.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Service result | `"enrolled"` | `"prerequisite_missing"` |
| Stored enrollment `e1` | An enrolled row | No row |

After `intro` is marked complete for `s1`, the same enrollment request should
succeed if a seat is available.

## Acceptance Criteria

- Every prerequisite must be complete before a learner joins either the course
  or its waitlist. A missing prerequisite must not create an enrollment row.
- Enrolled count never exceeds capacity. Eligible learners are enrolled when a
  place exists and waitlisted otherwise; waiting rows do not consume seats.
- A learner cannot have duplicate enrolled or waitlisted rows for one course,
  and an enrollment ID cannot replace another row.
- Dropping an active row marks it `dropped`. When an enrolled seat opens, the
  next waiting learner is promoted once without exceeding capacity. Repeating
  the drop fails and cannot promote another learner.
- Reject unknown courses and missing learner/enrollment IDs without changing
  the roster. Only recorded completions satisfy prerequisites.

## Out of Scope

Keep the repository's existing enrollment-ID ordering for waitlist selection.
Changing that ordering, scheduling courses, tuition, and notifying learners are
outside this ticket.

## Investigation

Trace the report, then compare enrolled and waitlisted rows in a full course
before and after a drop. Add regression cases for missing/completed prerequisites,
duplicate requests, and repeated drops. Assert stored statuses and enrolled counts.

## Starter Code

[View starter code](../../round-2/08-course-enrollment/)

## Reference Solution

[View solution](../../solutions/round-2/08-course-enrollment/)
