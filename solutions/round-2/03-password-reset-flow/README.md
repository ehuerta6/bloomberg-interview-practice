# Password Reset Flow Reference Solution

## What Was Broken?

An older reset link remained usable after a newer request for the same account.

## Reproduce the Behavior

From this folder, run `python3 test_password_reset.py`; `test_retry_invalidates_older_token_for_same_user` issues `first` and then `second` for `u1`. Try both links and inspect `password_hash("u1")`. The starter accepts the old link and stores `old-path`, even though the newer link was issued.

## Investigation

Trace `issue` and `reset` through the token repository. Compare token records after the second request; verify expiry at the exact boundary and verify a failed attempt leaves the password untouched. The tests check the stored records and state totals so the failure is visible at the domain boundary.

## Fix

A new token invalidates earlier unused tokens for the same user before it is saved. Reset validates existence, invalidation, single-use state, expiry, and input before changing the password; it marks the token used as part of the successful transition.

## Regression Tests

The corrected suite covers the reported failure, normal success, rejected and repeated requests, and state invariants. It also checks boundary or retry behavior with deterministic clocks and in-memory repositories. All assertions inspect returned results and persisted state.

## Run the Corrected Tests

```sh
python3 test_password_reset.py
```
