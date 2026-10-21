# Ticket #11 — Subscription Renewal

**Difficulty:** Medium

## Problem

### Reported symptom

Members are shown as current after a renewal charge was declined, and some renewal invoices appear to have been charged more than once.

### Scenario

A monthly subscription reaches its due date. The billing worker may retry an invoice after a timeout, and a declined payment should remain visible to account support until a later successful collection.

## Acceptance Criteria
- Each invoice identifier represents one charge attempt and replaying it does not charge twice.
- Only a successful charge advances the renewal date; a decline preserves the due date and marks the subscription past due.
- Invalid requests must leave persisted state unchanged.

## State Invariants

Only a successful charge advances the renewal date; a decline preserves the due date and marks the subscription past due.

## Investigation

Trace the invoice id through the renewal service and gateway. Compare subscription state before and after declined, successful, early, and repeated renewal requests. Add regression coverage for the behavior you reproduce.

## Starter Code

[View starter code](../../round-2/11-subscription-renewal/)

## Reference Solution

[View solution](../../solutions/round-2/11-subscription-renewal/)
