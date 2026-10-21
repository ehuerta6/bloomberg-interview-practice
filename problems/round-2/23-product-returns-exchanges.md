# Ticket #23 — Product Returns & Exchanges

**Difficulty:** Medium

## Problem

### Reported symptom

A store accepts customer returns for refunds or size exchanges. A failed replacement lookup left returned stock available even though no exchange was recorded, and customers could exceed the quantity purchased by splitting requests.

### Scenario

Exercise a refund and exchange from the same order line, then try exceeding the original purchased quantity. Force an exchange failure with no replacement stock and compare stock and return records before and after.

## Acceptance Criteria
- Refund amount equals returned quantity times the original unit price.
- Refund and exchange return the original SKU to stock.
- Exchange consumes replacement stock only when available.
- Failed requests make no stock or ledger changes.
- Return limits account for earlier refunds and exchanges combined.

## State Invariants
- A line cannot have more units returned than purchased.
- Every completed return case corresponds to exactly one stock and financial effect.
- Stock counts never become negative.
- Replaying a return ID cannot apply effects twice.

## Investigation

Trace a refund and an exchange against the same order line, then split additional returns until the purchased quantity would be exceeded. Force an unavailable replacement and replay a completed return ID; compare inventory, refund totals, and return records after each attempt.

## Starter Code

[View starter code](../../round-2/23-product-returns-exchanges/)

## Reference Solution

[View solution](../../solutions/round-2/23-product-returns-exchanges/)
