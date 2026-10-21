# Problem 08 — Movie Theater Seat Booking

**Difficulty:** Hard

## Scenario

A local theater wants customers to browse showings, choose specific seats, temporarily hold them while paying, and receive confirmed tickets after successful payment. A showing belongs to one auditorium, whose seats have stable identifiers. A seat cannot be sold twice for the same showing. Payment is handled by an external provider and may be delayed, fail, or send a repeated result notification.

## Functional Requirements

- Customers can browse upcoming showings and see which seats are available, held, or booked.
- A customer can request a set of seats for a showing. A successful hold reserves all requested seats together for a short, fixed period (assume five minutes).
- A customer can confirm a hold by paying. Tickets are issued only after confirmed payment.
- An expired hold releases its seats. A failed or cancelled payment also releases the seats if the hold is still active.
- A customer can retrieve tickets for their confirmed booking. The system must not expose another customer's booking.
- Duplicate payment callbacks must not issue duplicate tickets or charge the customer twice through the application's payment request flow.

## Constraints & Assumptions

- Start with one theater and a relational database. Seat counts are modest; correctness is more important than extreme throughput.
- Hold expiration is evaluated against server time. Clarify how payment completion racing with expiry is decided; assume the database transaction that confirms payment must verify the hold has not expired.
- The payment provider supports an idempotency key and sends a stable provider transaction identifier. Do not store card details.
- Refunds, dynamic pricing, seat recommendations, and multi-theater administration are out of scope.

## Your Task

Design seat availability and the hold-to-payment-to-ticket lifecycle. Explain how the model prevents two concurrent customers from holding the same seat, how an entire multi-seat request succeeds or fails atomically, and how expiration and provider retries affect state. Trace one booking from seat selection through ticket retrieval.

## Interviewer Follow-Ups

- Payment succeeds at the provider just as the hold expires. How do you reconcile the provider result and seat ownership?
- A customer refreshes the confirmation page repeatedly. How do you avoid duplicate payment requests and tickets?
- The theater adds accessible seats that can initially be held only by customers who request accessibility. What changes to the rules and model?

## Reference Solution

[View the reference solution](../solutions/system-design/08-movie-theater-seat-booking.md)
