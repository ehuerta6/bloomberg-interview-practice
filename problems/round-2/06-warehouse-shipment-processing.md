# Ticket #06 — Warehouse Shipment Processing

**Difficulty:** Hard

## Practice Metadata

- **Interview format:** Engineering ticket / existing-code debugging.
- **Primary skills:** stock rollback, reservation invariants, stateful regression testing.
- **Expected duration:** 50–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Reproduce a later-line stock shortage and prove that a rejected all-or-nothing shipment leaves every reservation and quantity unchanged.
- **Interviewer evaluation:** Problem decomposition, code navigation, root-cause explanation, incremental implementation, and test evidence. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

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
next order.

## Core acceptance criteria

- An all-or-nothing order ships every line or leaves on-hand quantities and
  reservations as they were before the attempt. Its backorder covers the
  unshipped request.
- Existing reservations reduce availability and must survive another order's
  failed attempt. Reserved stock never exceeds on-hand stock.
- A failed attempt leaves no reservation created by that attempt behind.


## Optional follow-ups

If the core rollback regression is complete, discuss partial fulfillment or an order retry. With partial fulfillment enabled on a fresh copy of the sample stock, the expected result is to ship 3 `sku-a` and 2 `sku-b`, leave on-hand quantities 1 and 0, and record a backorder of 1 `sku-b`. State the additional invariant each follow-up requires; neither is needed to finish the core interview task.

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
