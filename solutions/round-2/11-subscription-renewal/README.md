# Subscription Renewal Reference Solution

## What Was Broken

Members are shown as current after a renewal charge was declined, and some renewal invoices appear to have been charged more than once. The defect occurs because the workflow does not consistently preserve its key state invariant: only a successful charge advances the renewal date; a decline preserves the due date and marks the subscription past due.

## Reproduce and Investigate

From this folder, run `python3 test_subscription_renewal.py`. Compare the reported state with the state stored by the service. Then follow the request through its service, store, and provider or record types. The tests use in-memory state, so each run starts fresh.

## The Fix

The corrected service validates the request before mutation, persists state at the appropriate transition, and handles retries according to the stable event, invoice, transaction, session, or job identifier. Each invoice identifier represents one charge attempt and replaying it does not charge twice.

## Regression Coverage

The tests cover the reported failure, its successful path, and boundary or replay behavior. They assert persisted records and externally visible effects rather than implementation details.

## Run

```sh
python3 test_subscription_renewal.py
```
