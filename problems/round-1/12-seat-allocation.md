# PR #12 — Seat Reservation Conflict

**Difficulty:** Easy

## Practice Metadata

- **Interview format:** PR review / focused debugging.
- **Primary skills:** State conflict investigation, regression testing, communication.
- **Expected duration:** 35–45 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Trace one conflicting reservation attempt, prevent an existing reservation from being replaced, and verify the stored owner remains unchanged.
- **Interviewer evaluation:** Code investigation, observable state reasoning, a focused regression test, and a clear explanation of why this in-memory example does not prove concurrency safety. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

**PR title:** Prevent a second customer from replacing an existing seat reservation

## Summary

The event checkout service keeps a small reservation snapshot mapping seat IDs to customer IDs. Support reports that a second checkout can appear successful for a seat that another customer already reserved. You are reviewing the change that handles one reservation attempt.

## Expected behavior

- `reserve_seat(reservations, seat_id, customer_id)` returns `True` and records the customer when the seat is not present.
- If the seat already has a reservation, return `False` and preserve the existing customer.
- A conflict on one seat must not prevent a later reservation for a different seat.

The mapping is a single-process snapshot. Thread safety, persistence, payment handling, and multi-seat group allocation are outside this review.

## Reproduction

Starting with `{"A-12": "customer-1"}`, calling `reserve_seat(reservations, "A-12", "customer-2")` must return `False` and leave the mapping unchanged.

## Review task

Trace the reservation result and stored state for both an open seat and an already claimed seat. Correct the regression, add or refine a focused test that verifies the original owner remains recorded, and explain what this in-memory example proves and what it does not prove about concurrent requests.

## Starter Code

[View starter code](../../round-1/12-seat-allocation/)

## Optional algorithm extension

The earlier contiguous-group allocation exercise remains available as an optional extension in `round-1/12-seat-allocation/extensions/seat_allocation_algorithm.py`. It is separate from the 45-minute reservation review.

## Reference Solution

[View solution](../../solutions/round-1/12-seat-allocation/)
