# Ticket #23 — Product Returns & Exchanges

**Difficulty:** Medium

## Context

You maintain a shop's returns desk. An order line records the purchased SKU
(product identifier), quantity, and original unit price in cents. A refund
returns money; an exchange returns the original item and consumes replacement
stock. Return limits combine earlier refunds and exchanges for the same order line.

## Practice report

Order `o1` has line `l1`: 3 coats at 2500 cents each. Current stock is `coat=1`,
`shirt=4`, with no `missing` replacement SKU. Request one coat exchange using
`process("r1", "o1", "l1", 1, "exchange", "missing")` through the route adapter.

| Observation after rejection | Current starter | Expected |
| --- | --- | --- |
| Route status | 409 | 409 |
| Stock | `coat=2`, `shirt=4` | `coat=1`, `shirt=4` |
| Saved return cases | None | None |

A failed exchange must not make an additional coat available for sale.

## Acceptance Criteria

- Validate a new nonempty return ID, an existing order line, a positive integer
  quantity excluding booleans, and an action of `refund` or `exchange`.
- Returned quantity across earlier refunds and exchanges plus the new request
  cannot exceed the purchased quantity. Line IDs are scoped to their order.
- A refund restores the original SKU's quantity and returns exactly
  `quantity * original_unit_price` cents.
- An exchange requires a replacement SKU and enough replacement units. Success
  restores the original units, consumes the replacement units, returns zero
  refund cents, and records one completed return case.
- Any rejected request leaves stock and return records unchanged. Stock never
  becomes negative.
- A reused return ID is rejected with no second effect, including an exact replay.

## Out of Scope

Keep the local inventory and returned `refund_cents` result. Real payment
refunds, shipping, return eligibility dates, and exchange price differences are
outside this ticket.

## Investigation

Reproduce the unavailable replacement, then compare a successful exchange and
refund. Add tests for split returns reaching the purchase limit, replay, and the
same line ID on separate orders. Assert inventory, case records, and refund amounts.

## Starter Code

[View starter code](../../round-2/23-product-returns-exchanges/)

## Reference Solution

[View solution](../../solutions/round-2/23-product-returns-exchanges/)
