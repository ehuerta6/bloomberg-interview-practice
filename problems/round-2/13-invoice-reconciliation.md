# Ticket #13 — Invoice Reconciliation

**Difficulty:** Medium

## Problem

### Reported symptom

An invoice is marked paid before all funds arrive, and duplicate bank notifications can make the recorded amount exceed the remittance.

### Scenario

A customer pays an invoice in installments. Bank notifications can be delivered more than once, and each payment reference must reconcile to one invoice and amount.

## Acceptance Criteria
- Partial payments accumulate until the invoice’s exact balance is settled.
- A payment reference is applied at most once, and overpayments are rejected without changing invoice or payment records.
- Invalid requests must leave persisted state unchanged.

## State Invariants

A payment reference is applied at most once, and overpayments are rejected without changing invoice or payment records.

## Investigation

Trace bank reference lookup, invoice balance calculation, and payment persistence. Test partial settlement, duplicate notices, unknown invoices, and an amount larger than the remaining balance. Add regression coverage for the behavior you reproduce.

## Starter Code

[View starter code](../../round-2/13-invoice-reconciliation/)

## Reference Solution

[View solution](../../solutions/round-2/13-invoice-reconciliation/)
