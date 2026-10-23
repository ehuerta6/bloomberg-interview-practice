# Ticket #11 — Subscription Renewal

**Difficulty:** Medium

## Context

You maintain monthly membership billing. A subscription has a scheduled due date
and a fee in cents. An invoice ID identifies one collection attempt; replaying
an invoice returns its saved outcome. A later collection after a decline uses
a new invoice ID. The gateway in this exercise is a configurable fake.

## Practice report

Create active subscription `sub-1` for 1200 cents, due `2026-10-01`. Configure
the gateway to decline and call `renew("sub-1", "invoice-2", "2026-10-01")`.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Renewal result and saved invoice | `declined` | `declined` |
| Subscription status | `active` | `past_due` |
| Next due date | `2026-10-01` | `2026-10-01` |

Support needs the subscription status to agree with the unpaid renewal.

## Acceptance Criteria

- Charge only a due subscription whose status is `active` or `past_due`.
  Early or canceled-subscription requests return `not_due` without a charge;
  an unknown subscription returns `missing` without creating an invoice.
- A decline saves the invoice as `declined`, marks the subscription `past_due`,
  and preserves its scheduled due date.
- A successful charge saves a `paid` invoice, sets the subscription `active`,
  and advances the scheduled due date by one month. Clamp the day to the last
  valid day of the target month; January 31, 2026 advances to February 28, 2026.
- Replaying a recorded paid or declined invoice returns that outcome without
  another charge or date change. A newly identified attempt can collect after
  a decline and restore the subscription to active.
- Rejected early, canceled, or missing-subscription requests preserve stored
  subscription and invoice state.

## Out of Scope

Use ISO date strings and the included gateway. Proration, payment-method
management, invoice ownership across subscriptions, and real payment retries are
outside this ticket.

## Investigation

Trace invoice outcomes, gateway calls, and subscription state on decline,
success, replay, and an early request. Add focused tests that assert the due
date and status together, including a new invoice after a decline and a
month-end renewal.

## Starter Code

[View starter code](../../round-2/11-subscription-renewal/)

## Reference Solution

[View solution](../../solutions/round-2/11-subscription-renewal/)
