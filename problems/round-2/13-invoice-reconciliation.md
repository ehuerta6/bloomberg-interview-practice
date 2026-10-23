# Ticket #13 — Invoice Reconciliation

**Difficulty:** Medium

## Context

You maintain invoice reconciliation for a finance tool. Reconciliation matches
a payment notification to an invoice and updates its amount paid. A payment ID
is the bank's reference for one remittance; repeating its notification must not
count the funds twice. Amounts are in cents.

## Practice report

Create `inv-1` with total 10000 and paid amount 0. Apply
`apply_payment("pay-3", "inv-1", 4000)` twice.

| Observation after both notifications | Current starter | Expected |
| --- | --- | --- |
| Invoice paid amount | 8000 | 4000 |
| Stored payment count for the invoice | 1 | 1 |
| Invoice status | `partial` | `partial` |

Compare the paid amount with the actual saved remittance, rather than relying
only on the number of records.

## Acceptance Criteria

- Positive installments accumulate against the remaining invoice balance.
  A smaller installment leaves `partial`; exact settlement changes it to `paid`.
- Apply one payment reference at most once. An identical replay preserves the
  paid amount and payment record and returns the current partial/paid outcome.
- With an existing target invoice and a positive amount, reusing a reference
  for different payment details returns `conflict` without replacing the original
  payment or changing either invoice.
- Unknown invoices, nonpositive amounts, new payments against a paid invoice,
  and overpayments are rejected without invoice or payment-record changes.
- The paid amount cannot exceed the invoice total, including across multiple
  notifications and retries.

## Out of Scope

Use the existing local store and payment amounts. Bank integration, currency
conversion, automatic refunds, and expanding amount-type validation are outside
this ticket.

## Investigation

Trace the duplicate report through the invoice and payment stores. Add focused
tests for two installments that settle exactly, a replay, changed details under
one reference, and an overpayment. Assert paid amounts and saved payment details
after both accepted and rejected calls.

## Starter Code

[View starter code](../../round-2/13-invoice-reconciliation/)

## Reference Solution

[View solution](../../solutions/round-2/13-invoice-reconciliation/)
