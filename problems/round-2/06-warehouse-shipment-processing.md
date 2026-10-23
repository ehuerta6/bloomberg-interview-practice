# Ticket #06 — Warehouse Shipment Processing

**Difficulty:** Hard

## Context

You maintain a warehouse's shipment service. A **SKU** is an identifier for one
stock item, such as `sku-a`. **Stock on hand** is the quantity physically in the
warehouse. **Reserved** units are held for orders and are still on hand but
cannot be promised again. **Available** units equal on-hand minus reserved units.

`fulfill(order_id, lines, allow_partial=False)` receives a mapping from SKU to
requested quantity. **All-or-nothing** means every requested unit ships or none
ships. **Partial fulfillment** ships available units; a **backorder** records the
requested units that could not ship.

## Practice report

Start with no reservations and stock `sku-a=4`, `sku-b=2`. Call
`fulfill("o1", {"sku-a": 3, "sku-b": 3})` in that line order.

| Point in the request | `sku-a` | `sku-b` |
| --- | --- | --- |
| On hand before the request | 4 | 2 |
| Reserved before the request | 0 | 0 |
| Requested, all-or-nothing | 3 | 3 |
| Current starter after returning `backordered` | 4 on hand; 3 reserved | 2 on hand; 0 reserved |
| Expected after the failed attempt | 4 on hand; 0 reserved | 2 on hand; 0 reserved |

The unsuccessful order must not leave those 3 `sku-a` units unavailable to the
next order. On a fresh copy of the same stock, allowing partial fulfillment
instead should ship 3 `sku-a` and 2 `sku-b`, leave on-hand quantities 1 and 0,
and record a backorder of 1 `sku-b`.

## Acceptance Criteria

- An all-or-nothing order ships every line or leaves on-hand quantities and
  reservations as they were before the attempt. Its backorder covers the
  unshipped request.
- Existing reservations reduce availability and must survive another order's
  failed attempt. Reserved stock never exceeds on-hand stock.
- A failed attempt leaves no reservation created by that attempt behind.
- With partial fulfillment enabled, ship only available units and record each
  unshipped remainder. Shipped plus backordered units equal requested units.
- Retrying a shipped or partially shipped order returns `already_shipped`
  without deducting stock again.
- Reject empty requests and invalid quantities before stock changes. Quantities
  must satisfy the existing positive-integer contract; zero, negative, and
  non-integer quantities are rejected.

## Out of Scope

Keep the supplied repository and recorded backorders. Purchasing replacement
stock, automatically retrying backorders, shipping-carrier APIs, and database
concurrency are outside this ticket.

## Investigation

Reproduce both modes from separate fresh repositories. Trace the service and
warehouse records, then prove the stock and reservation invariants with tests
for a shortage on a later line, pre-existing reservations, invalid quantities,
and completed-order retries. Explain the state before and after each request.

## Starter Code

[View starter code](../../round-2/06-warehouse-shipment-processing/)

## Reference Solution

[View solution](../../solutions/round-2/06-warehouse-shipment-processing/)
