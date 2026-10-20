# Checkout Promotion Engine Reference Solution

## What Was Broken

Some shoppers receive a discount for products the promotion excludes, and the displayed tax and final total do not agree with the cart. The defect occurs because the workflow does not consistently preserve its key state invariant: the discount cannot exceed the eligible amount; tax is calculated after the discount and the final total never becomes negative.

## Reproduce and Investigate

From this folder, run `python3 test_promotion_engine.py`. Compare the reported state with the state stored by the service. Then follow the request through its service, store, and provider or record types. The tests use in-memory state, so each run starts fresh.

## The Fix

The corrected service validates the request before mutation, persists state at the appropriate transition, and handles retries according to the stable event, invoice, transaction, session, or job identifier. Promotion eligibility and minimum subtotal determine whether a discount applies.

## Regression Coverage

The tests cover the reported failure, its successful path, and boundary or replay behavior. They assert persisted records and externally visible effects rather than implementation details.

## Run

```sh
python3 test_promotion_engine.py
```
