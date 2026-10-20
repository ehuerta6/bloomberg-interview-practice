# Digital Wallet Ledger Reference Solution

## What Was Broken

A wallet transfer is reflected twice in balances after a client retries, and the transaction history no longer balances. The defect occurs because the workflow does not consistently preserve its key state invariant: a rejected or repeated transfer leaves balances and ledger history unchanged; a wallet cannot be overdrawn.

## Reproduce and Investigate

From this folder, run `python3 test_wallet_ledger.py`. Compare the reported state with the state stored by the service. Then follow the request through its service, store, and provider or record types. The tests use in-memory state, so each run starts fresh.

## The Fix

The corrected service validates the request before mutation, persists state at the appropriate transition, and handles retries according to the stable event, invoice, transaction, session, or job identifier. Every posted transfer has exactly two entries with equal and opposite amounts.

## Regression Coverage

The tests cover the reported failure, its successful path, and boundary or replay behavior. They assert persisted records and externally visible effects rather than implementation details.

## Run

```sh
python3 test_wallet_ledger.py
```
