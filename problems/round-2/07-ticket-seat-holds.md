# Ticket #07 — Ticket Seat Holds

**Difficulty:** Medium

## Practice Metadata

- **Interview format:** Engineering ticket / existing-code debugging.
- **Primary skills:** code navigation, state invariants, regression testing, implementation judgment.
- **Expected duration:** 50–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Trace the reported behavior through the supplied code, state an invariant, make a focused change, and prove it with a regression test.
- **Interviewer evaluation:** Problem decomposition, code navigation, root-cause explanation, incremental implementation, and test evidence. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

## Context

You maintain temporary seat reservations for event checkout. A hold gives one
buyer a short opportunity to purchase one seat. Confirmation turns an unexpired
hold into a booking; a confirmed seat must remain unavailable after the original
hold deadline.

## Practice report

At 12:00 on 2030-01-01, hold `A1` for `buyer-a` under `h1`, using the default
five-minute lifetime. At exactly 12:05, call `hold("A1", "buyer-b", "h2")`.

| Observation | Current starter | Expected |
| --- | --- | --- |
| New hold result | `False` | `True` |
| Owner stored for seat `A1` | `buyer-a` | `buyer-b` |

Use the injected clock to reproduce this without sleeping.

## Acceptance Criteria

- A seat has at most one live hold or confirmed booking. Before expiry, a
  competing buyer cannot take the seat.
- An unconfirmed hold expires at its deadline: it must stop blocking a new
  buyer at that instant and afterward.
- A live hold ID cannot be reused to claim a second seat. Rejected requests
  preserve existing seat and hold ownership.
- Only the owning buyer can confirm an unexpired, unconfirmed hold.
- Confirmation keeps the seat unavailable permanently for this exercise;
  passing the temporary hold deadline does not release a confirmed booking.
- Unknown seats, missing buyer/hold IDs, and unavailable confirmations fail
  without replacing an existing booking.

## Out of Scope

Keep the supplied seats and clock. Payments, booking cancellation, seat maps,
and multiple-process locking are outside this ticket.

## Investigation

Trace holding and confirmation around the deadline. Add tests immediately
before and exactly at expiry, a competing buyer, hold-ID reuse, and confirmation
by the wrong buyer. Assert the stored owner, not just the returned boolean.

## Starter Code

[View starter code](../../round-2/07-ticket-seat-holds/)

## Reference Solution

[View solution](../../solutions/round-2/07-ticket-seat-holds/)
