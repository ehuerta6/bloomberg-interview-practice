# PR #23 — Reservation Expiration

**Difficulty:** Medium

## PR title

Expire reservations at their deadline

## Summary

An inventory service places items on hold while a customer completes a reservation. A cleanup call must mark pending holds as expired once their deadline arrives, while leaving confirmed or already-expired records alone. You are reviewing the expiration PR; the function returns updated copies for its caller to use and a list of transitions made in this call.

## Input and output

`expire_reservations(reservations, now)` accepts reservation dictionaries with `reservation_id`, `status`, and an ISO 8601 `expires_at` timestamp. `now` is a `datetime`. It returns a dictionary with copied `reservations` and an `expired_ids` list of IDs transitioned during this call.

## Expected behavior, edge cases, and invariants
- Only records with status `pending` can transition to `expired`.
- A reservation expires when `expires_at` is less than or equal to `now`.
- List newly expired IDs in input order. Do not mutate input records.
- Reject malformed records and comparisons that mix timezone-aware and naive datetimes with `ValueError`.

## Contract example

Let `now=datetime(2025, 1, 1, 12, 0, 0)`. The timestamps in this example have no timezone offset, matching `now`.

| Input ID | Initial status | `expires_at` | Returned status | In `expired_ids`? |
| --- | --- | --- | --- | --- |
| `"r1"` | `"pending"` | `"2025-01-01T11:59:00"` | `"expired"` | Yes |
| `"r2"` | `"pending"` | `"2025-01-01T12:00:00"` | `"expired"` | Yes |
| `"r3"` | `"pending"` | `"2025-01-01T12:01:00"` | `"pending"` | No |
| `"r4"` | `"confirmed"` | `"2025-01-01T11:00:00"` | `"confirmed"` | No |

For these records in this order, `expired_ids` is `["r1", "r2"]`. The input records keep their original statuses. Calling again with the returned records at the same `now` reports no new expirations.

## Review task

Review the transition results and assertions against the deadline, eligible status, and copied-output contract. Correct discrepancies and add cases for the exact deadline, a repeated call, input isolation, and incompatible timezone styles. Explain how the tests distinguish a newly expired hold from a record that was already complete.

## Starter Code

[View starter code](../../round-1/23-reservation-expiration/)

## Reference Solution

[View solution](../../solutions/round-1/23-reservation-expiration/)
