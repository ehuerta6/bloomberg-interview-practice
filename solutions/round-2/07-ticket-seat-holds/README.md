# Ticket Seat Holds Reference Solution

## What Was Broken?

An expired hold continued to block a seat from a new buyer.

## Reproduce the Behavior

From this folder, run `python3 test_holds.py`; `test_expired_hold_releases_seat` advances the injected clock by exactly five minutes and asks a second buyer to hold `A1`. The starter continues to treat the first hold as active.

## Investigation

Use the injected clock to compare a hold immediately before and exactly at its five-minute expiry. Follow the hold record and seat lookup for the original buyer, a second buyer, and a confirmed booking; the expiry rule must not free a confirmed seat or let another buyer confirm someone else's hold.

## Fix

A hold is active only while confirmed or before its expiry time. Expired holds can be removed and replaced; live identifiers, confirmed seats, and ownership remain protected.

## Regression Tests

The tests cover a live hold, expiration at the boundary, replacement by a second buyer, confirmation, duplicate hold IDs, and attempts to use another buyer's hold. They inspect stored hold and confirmed-booking state so capacity remains consistent across retries.

## Run the Corrected Tests

```sh
python3 test_holds.py
```
