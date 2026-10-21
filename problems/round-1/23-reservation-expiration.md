# PR #23 — Reservation Expiration

**Difficulty:** Medium

## PR title

Expire reservations at their deadline

## Summary

An inventory hold should be released when its deadline is reached. Review how the service transitions pending reservations while preserving active and completed records.

## Input and output

`expire_reservations(reservations, now)` accepts reservation dictionaries with `reservation_id`, `status`, and an ISO 8601 `expires_at` timestamp. `now` is a `datetime`. It returns a dictionary with copied `reservations` and an `expired_ids` list of IDs transitioned during this call.

## Expected behavior, edge cases, and invariants
- Only records with status `pending` can transition to `expired`.
- A reservation expires when `expires_at` is less than or equal to `now`.
- List newly expired IDs in input order. Do not mutate input records.
- Reject malformed records and comparisons that mix timezone-aware and naive datetimes with `ValueError`.

## Review task

Check the exact-deadline boundary, future reservations, confirmed and already-expired records, input immutability, ID ordering, and timezone compatibility.


## Starter Code

[View starter code](../../round-1/23-reservation-expiration/)

## Reference Solution

[View solution](../../solutions/round-1/23-reservation-expiration/)
