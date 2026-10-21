# Refund Processing Reference Solution

## What Was Broken?

An authorized but uncaptured payment could receive a refund.

## Reproduce the Behavior

From this folder, run `python3 test_refunds.py`; `test_uncaptured_or_unknown_payment_cannot_be_refunded` adds `p2` in `authorized` state and requests a 100-unit refund. The starter records the refund even though capture has not happened.

## Investigation

Follow the service from payment lookup through payment-state eligibility and refund-record creation. Compare the payment's refunded total and status before and after an accepted refund, an over-refund, a replay with the same refund ID, and a request against an authorized but uncaptured payment.

## Fix

Refunds are accepted only for captured or partially refunded payments. The service checks amount bounds and identifier reuse before recording a refund, then derives payment state from the total refunded amount.

## Regression Tests

The tests cover refunds from captured payments, partial and full refund totals, uncaptured and unknown payments, amounts beyond the remaining balance, exact idempotent retries, conflicting refund-ID reuse, and invalid amounts. They verify that rejected requests do not append a refund or change payment state.

## Run the Corrected Tests

```sh
python3 test_refunds.py
```
