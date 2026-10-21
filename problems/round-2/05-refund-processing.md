# Ticket #05 — Refund Processing

**Difficulty:** Medium

## Problem

### Reported symptom

A refund request can succeed for a payment that has not reached a refundable payment state.

### Scenario

Support submits refunds through an in-memory payment ledger. Requests can be retried after a slow response, and one captured payment can receive multiple partial refunds.

## Acceptance Criteria
- Only captured or partially refunded payments are eligible.
- Refund amounts must be positive and their total cannot exceed the captured amount.
- A repeated request with the same refund identifier and details has no additional effect.
- A refund identifier cannot be reused for different payment details.
- Successful refunds update both the refund ledger and payment state.

## State Invariants
- The sum of refunds for a payment never exceeds its captured amount.
- Rejected requests do not change the payment or refund ledger.
- A fully refunded payment cannot accept another refund.

## Investigation

Trace a refund from eligibility checks through ledger mutation. Compare captured and authorized payments, then retry identical and conflicting identifiers while inspecting both payment state and totals.

## Starter Code

[View starter code](../../round-2/05-refund-processing/)

## Reference Solution

[View solution](../../solutions/round-2/05-refund-processing/)
