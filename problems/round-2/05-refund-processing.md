# Ticket #05 — Refund Processing

**Difficulty:** Medium

## Context

You maintain a support tool for refunding payments. An `authorized` payment has
approval to charge but has not been captured; a `captured` payment has collected
funds. A partial refund returns some of those funds. Amounts use the integer
units already stored in the payment ledger.

## Practice report

Add payment `p2` with amount 900 and state `authorized`. Request
`refund("p2", "rf2", 100)`.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Service result | `"refunded"` | `"rejected"` |
| Refunded total | 100 | 0 |
| Payment state | `partially_refunded` | `authorized` |

A refund ID identifies one refund request. An identical retry must have no
additional effect; using that ID for different payment details is a conflict.

## Acceptance Criteria

- New refunds are eligible only for `captured` or `partially_refunded` payments.
  Unknown payments and payments in other states are rejected.
- Amounts must be positive integers. Cumulative refunds cannot exceed the
  payment amount, including when several partial refunds are requested.
- A successful request records one refund and sets the payment to
  `partially_refunded` or, at exact full refund, `refunded`.
- An exact refund-ID replay returns `already_refunded` without another ledger
  effect. Reusing that ID for a different payment or amount is rejected.
- Rejected requests leave payment state and refund records unchanged. A fully
  refunded payment cannot accept a new refund.

## Out of Scope

Use the included ledger. Bank transfers, currency conversion, external refund
providers, and asynchronous settlement are outside this ticket.

## Investigation

Trace the report from payment lookup to the saved refund and payment state.
Compare an uncaptured payment with a captured one, then test partial totals,
exact settlement, over-refunds, and repeated IDs. Assert ledger contents as well
as result strings.

## Starter Code

[View starter code](../../round-2/05-refund-processing/)

## Reference Solution

[View solution](../../solutions/round-2/05-refund-processing/)
