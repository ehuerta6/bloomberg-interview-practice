# Ticket Seat Holds Reference Solution

## What Was Broken?

An expired hold continued to block a seat from a new buyer.

## Reproduce the Behavior

From this folder, run `python3 test_holds.py`; `test_expired_hold_releases_seat` advances the injected clock by exactly five minutes and asks a second buyer to hold `A1`. The starter continues to treat the first hold as active.

## Investigation

Use the injected clock to inspect the hold at its expiry boundary. Compare a temporary hold, an expired hold, and a confirmed hold while checking ownership and seat availability. The tests check the stored records and state totals so the failure is visible at the domain boundary.

## Fix

A hold is active only while confirmed or before its expiry time. Expired holds can be removed and replaced; live identifiers, confirmed seats, and ownership remain protected.

## Regression Tests

The corrected suite covers the reported failure, normal success, rejected and repeated requests, and state invariants. It also checks boundary or retry behavior with deterministic clocks and in-memory repositories. All assertions inspect returned results and persisted state.

## Run the Corrected Tests

```sh
python3 test_holds.py
```
