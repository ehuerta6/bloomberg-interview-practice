# Reservation Expiration — Reference Solution

## What broke

The draft uses `expires_at < now`, so a pending reservation whose deadline equals `now` stays pending and is omitted from `expired_ids`. It also compares timestamps before checking timezone style, leaking `TypeError` for an aware expiration and naive `now`.

## Reproduce the issue

From `round-1/23-reservation-expiration/`, run `python3 reservations.py`. `test_exact_deadline_is_expired` fails because the record remains pending; `test_naive_and_aware_times_are_not_mixed` errors with `TypeError` rather than receiving `ValueError`. Run it in this solution folder to confirm both cases pass.

## Investigation approach

In `expire_reservations`, follow the parsed `expires_at` into the `status == "pending"` condition. The strict comparison explains the exact-deadline result. Separately, compare the timestamp's `tzinfo` with `now.tzinfo` before ordering them; Python raises `TypeError` when one datetime is aware and the other is naive.

## Correction

The solution validates `now`, parses and copies each record, rejects mismatched timezone styles with `ValueError`, and transitions only pending records where `expires_at <= now`. It appends IDs at the moment of transition, preserving input order, and leaves caller-owned dictionaries unchanged.

## Regression tests

`test_exact_deadline_is_expired` and `test_naive_and_aware_times_are_not_mixed` cover the two defects. Other cases check a future reservation, confirmed and already-expired records, newly expired ID order, and input immutability. Run them with `python3 reservations.py`.
