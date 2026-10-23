# Ticket #02 — Order Processing

**Difficulty:** Medium

## Context

You maintain a club merchandise checkout. `place_order(order_id, student_id,
item, quantity)` requests one item type. A reservation temporarily holds units
for that order; the included fake payment service records authorization calls
and can be configured to approve or decline them.

## Practice report

Start with 5 `club-shirt` units and a payment service configured to decline.
Submit order `o1` for student `s1`, requesting 2 shirts through the route adapter.

| Observation after the request | Current starter | Expected |
| --- | --- | --- |
| Route status and saved order state | 409; `failed` | 409; `failed` |
| Available shirts | 3 | 5 |

Also submit a successful order twice with the same ID. A client retry must
return its completed result without another inventory deduction or payment call.

## Acceptance Criteria

- Require nonempty string order, student, and item IDs and a positive integer
  quantity; booleans and non-integer quantities are invalid. Missing route
  fields return 400; rejected orders return 409 without inventory or payment effects.
- Insufficient stock leaves quantities unchanged and makes no payment call.
  Available inventory never becomes negative.
- A declined payment leaves a failed order, restores available inventory, and
  leaves no outstanding reservation from the attempt.
- A successful order becomes `completed`, deducts its quantity once, and leaves
  no outstanding reservation. An exact completed-order retry returns success
  without another deduction or authorization.
- A failed order can be tried again after the fake payment service recovers;
  the final quantities must reflect only the successful purchase.

## Out of Scope

Use the supplied in-memory payment fake and repositories. Real card payments,
shipping, multi-item baskets, and distributed transactions are outside this ticket.

## Investigation

Trace the declined and successful requests through the route, order service,
inventory, payment fake, and repository. Add tests that compare quantities,
reservations, payment call counts, and order state before and after failure and
retry. Replace assertions that do not observe the request's effects.

## Starter Code

[View starter code](../../round-2/02-order-processing/)

## Reference Solution

[View solution](../../solutions/round-2/02-order-processing/)
