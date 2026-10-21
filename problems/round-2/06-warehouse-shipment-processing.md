# Ticket #06 — Warehouse Shipment Processing

**Difficulty:** Hard

## Problem

### Reported symptom

A multi-item order that cannot ship in full leaves some stock unavailable to later orders.

### Scenario

A warehouse fulfills orders containing several SKUs. Inventory may already be reserved for another order, and operations may permit shipping available lines while backordering the remainder.

## Acceptance Criteria
- An all-or-nothing order either reserves and ships every line or leaves stock unchanged.
- Existing reservations reduce the quantity available to new orders.
- A failed fulfillment releases every reservation made during that attempt.
- When partial fulfillment is allowed, only available units ship and the remainder is recorded as a backorder.
- Retrying a completed order does not deduct stock a second time.
- Invalid quantities are rejected before stock changes.

## State Invariants
- Reserved stock never exceeds on-hand stock.
- A failed all-or-nothing attempt leaves pre-existing stock and reservations unchanged.
- Shipped plus backordered quantities equal the requested quantities.

## Investigation

Trace a two-SKU order where the first line is available and a later line is short. Inspect stock, reservations, and shipment records before and after failure, then compare partial and complete fulfillment.

## Starter Code

[View starter code](../../round-2/06-warehouse-shipment-processing/)

## Reference Solution

[View solution](../../solutions/round-2/06-warehouse-shipment-processing/)
