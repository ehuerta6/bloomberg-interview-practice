# Session Revocation Reference Solution

## What Was Broken

A user logs out, but the same session token still opens protected pages; logging out on one device must not sign out all devices. The defect occurs because the workflow does not consistently preserve its key state invariant: revocation is scoped to one session, persisted, and idempotent; another device’s session remains active.

## Reproduce and Investigate

From this folder, run `python3 test_session_revocation.py`. Compare the reported state with the state stored by the service. Then follow the request through its service, store, and provider or record types. The tests use in-memory state, so each run starts fresh.

## The Fix

The corrected service validates the request before mutation, persists state at the appropriate transition, and handles retries according to the stable event, invoice, transaction, session, or job identifier. A revoked session is no longer authorized for protected access.

## Regression Coverage

The tests cover the reported failure, its successful path, and boundary or replay behavior. They assert persisted records and externally visible effects rather than implementation details.

## Run

```sh
python3 test_session_revocation.py
```
