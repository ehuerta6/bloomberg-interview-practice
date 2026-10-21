# Ticket #02 — Order Processing

**Difficulty:** Medium

## Problem

### Reported symptom

A customer reports that inventory becomes unavailable after an order fails during payment. Investigate the order flow across the route, order service, payment adapter, inventory, and repository.

### Relevant scenario

A request reserves items, calls an in-memory fake payment adapter, and either completes or fails. The client may retry after an uncertain response, using the same order identifier.

## Acceptance Criteria
- Invalid orders fail without corrupting state.
- Failed payment authorization does not permanently reduce available inventory.
- A successful order does not deduct inventory more than once.
- Retrying a completed order with the same identifier does not duplicate its effects.
- Payment uses the included in-memory fake; no external service is needed.

## State Invariants
- Available inventory cannot become negative.
- Each order identifier produces at most one completed order and one corresponding inventory deduction.
- Failure and retry paths leave payment, order, and inventory state consistent.

## Investigation

Follow one order from request validation through inventory and payment state changes. Identify what happens on success, failure, and retry. Check whether the tests assert the inventory invariant and would catch a regression. Make a focused fix and add tests for the state transitions you verify.

## Starter Code

[View starter code](../../round-2/02-order-processing/)

## Reference Solution

[View solution](../../solutions/round-2/02-order-processing/)
