# Refund Processing Reference Solution

## What Was Broken?

An authorized but uncaptured payment could receive a refund.

## Reproduce the Behavior

From this folder, run `python3 test_refunds.py`; `test_uncaptured_or_unknown_payment_cannot_be_refunded` adds `p2` in `authorized` state and requests a 100-unit refund. The starter records the refund even though capture has not happened.

## Investigation

Follow the service from payment lookup through eligibility, refund-id lookup, and ledger mutation. Check state and aggregate totals after success, rejection, exact retries, and conflicting reuse of a refund identifier. The tests check the stored records and state totals so the failure is visible at the domain boundary.

## Fix

Refunds are accepted only for captured or partially refunded payments. The service checks amount bounds and identifier reuse before recording a refund, then derives payment state from the total refunded amount.

## Regression Tests

The corrected suite covers the reported failure, normal success, rejected and repeated requests, and state invariants. It also checks boundary or retry behavior with deterministic clocks and in-memory repositories. All assertions inspect returned results and persisted state.

## Run the Corrected Tests

```sh
python3 test_refunds.py
```
