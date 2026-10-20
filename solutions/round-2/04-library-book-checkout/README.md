# Library Book Checkout Reference Solution

## What Was Broken?

Returning a copy did not make it available to another reader because its loan still counted as active.

## Reproduce the Behavior

From this folder, run `python3 test_library.py`; in `test_return_releases_copy_and_cannot_be_repeated`, check out the only copy as `l1`, return it, then query `available_copies("b1")`. The starter still counts the loan as active, so the next reader cannot check it out.

## Investigation

Compare `available_copies` before checkout, after checkout, and after return. Follow the loan record status and test that a queued reader receives priority when a copy returns. The tests check the stored records and state totals so the failure is visible at the domain boundary.

## Fix

A successful return marks the loan closed, so active-loan counts release that copy. Checkout respects the head of the reservation queue, consumes the reservation only for its owner, and rejects repeated loan identifiers.

## Regression Tests

The corrected suite covers the reported failure, normal success, rejected and repeated requests, and state invariants. It also checks boundary or retry behavior with deterministic clocks and in-memory repositories. All assertions inspect returned results and persisted state.

## Run the Corrected Tests

```sh
python3 test_library.py
```
