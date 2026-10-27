# PR #02 — Event Scheduler

**Difficulty:** Medium

## Practice Metadata

- **Interview format:** PR review / focused debugging.
- **Primary skills:** event ordering, date/time reasoning, regression testing.
- **Expected duration:** 45–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Compare the proposed change and its tests with the observable contract, then make a targeted correction and regression test.
- **Interviewer evaluation:** Clarifying questions, code investigation, root-cause reasoning, maintainable changes, testing, and communication. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

**PR title:** Check event availability

## Summary

A club organizer wants to check whether a proposed event fits the schedule before booking it. You are reviewing `is_available(events, start, end)`, which returns a boolean for a list of existing `(start, end)` pairs. An availability check must leave booking state unchanged.

## Expected behavior
- Each event is represented by a start and end time and covers the half-open interval `[start, end)`.
- Adjacent events are allowed; an event ending at time `12` does not conflict with one starting at `12`.
- Any actual overlap is rejected.
- An interval with `start >= end` is invalid and rejected.
- Checking availability does not modify the existing event collection.

## Contract examples

With existing events `[(10, 12)]`, evaluate each candidate independently:

| Candidate `(start, end)` | Expected return | Existing events afterward |
| --- | --- | --- |
| `(12, 14)` | `True` | `[(10, 12)]` |
| `(11, 13)` | `False` | `[(10, 12)]` |
| `(5, 5)` | `False` | `[(10, 12)]` |

The interval notation `[10, 12)` includes time `10` and excludes time `12`; it does not reserve the next event's start.

## Review task

Review whether the implementation and tests distinguish touching intervals from overlapping ones. Correct contract violations and misleading assertions, then add regression cases that verify both the availability result and the event collection after a check.

## Starter Code

[View starter code](../../round-1/02-event-scheduler/)

## Reference Solution

[View solution](../../solutions/round-1/02-event-scheduler/)
