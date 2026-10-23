# Problem 02 — Campus Café Mobile Ordering

**Difficulty:** Medium

## Scenario

A campus café wants students to order ahead during the lunch rush. Students browse the menu, submit and pay for an order, then check its progress. Café staff need a screen showing incoming orders and a way to update each order as it moves through preparation. The first release serves one café location.

Adapted from Noel's CIC workshop. This is an educational exercise, not an official Bloomberg interview question.

## Functional Requirements

- Students can browse menu items, prices, and whether each product is currently available.
- Students can submit an order with one or more menu items and quantities, then pay through a payment provider.
- Sold-out items cannot be ordered. Stock counts must not become negative when orders arrive concurrently.
- Staff can view incoming orders and move paid orders through forward-only statuses: `PLACED`, `PREPARING`, `READY`, and `PICKED_UP`.
- Students can view the current status of their own order.
- A student may cancel only before preparation begins. A cancelled order cannot later advance through preparation statuses. `CANCELLED` is a separate terminal status.
- The order must retain the price charged for each item at placement time, even if the menu price changes later.

## Constraints & Assumptions

- Start with one café; multiple branches and delivery are out of scope.
- Assume a payment provider supports a request and a later success/failure result. Clarify whether the order is created before payment confirmation and how abandoned checkout is represented.
- Do not store card details. The provider owns payment credentials and processing.
- Define whether menu stock is tracked per item as a count or as simply available/unavailable. For this exercise, assume a count of sellable portions.
- Clarify the policy for restoring stock after a permitted cancellation and for a payment failure.
- No traffic, uptime, or real-time update target is supplied; polling the order status is acceptable initially.

## Your Task

Design the student, staff, and payment flows. Identify the records and keys needed to preserve a placed order's item names/prices and to prevent stock overselling. Walk through checkout, payment outcome, staff status changes, and a cancellation request. Explain which state transitions are legal and what must be atomic.

## Example to Work Through

Only one portion of a menu item remains when two students submit orders for it. Walk through what each student sees, then describe the order and payment records if the provider accepts payment but the café service times out before recording the result.

## Interviewer Follow-Ups

- The payment provider succeeds but the café service times out before saving the result. How can a retry avoid charging the student twice?
- Two students order the last portion of the same item concurrently. Where is availability checked and committed?
- Staff accidentally try to change a `READY` order back to `PREPARING`. How should the system respond?

## Reference Solution

[View the reference solution](../solutions/system-design/02-campus-cafe-ordering.md)
