# Invoice Reconciliation Reference Solution

## What Was Broken

An invoice is marked paid before all funds arrive, and duplicate bank notifications can make the recorded amount exceed the remittance. The defect occurs because the workflow does not consistently preserve its key state invariant: a payment reference is applied at most once, and overpayments are rejected without changing invoice or payment records.

## Reproduce and Investigate

From this folder, run `python3 test_invoice_reconciliation.py`. Compare the reported state with the state stored by the service. Then follow the request through its service, store, and provider or record types. The tests use in-memory state, so each run starts fresh.

## The Fix

The corrected service validates the request before mutation, persists state at the appropriate transition, and handles retries according to the stable event, invoice, transaction, session, or job identifier. Partial payments accumulate until the invoice’s exact balance is settled.

## Regression Coverage

The tests cover the reported failure, its successful path, and boundary or replay behavior. They assert persisted records and externally visible effects rather than implementation details.

## Run

```sh
python3 test_invoice_reconciliation.py
```
