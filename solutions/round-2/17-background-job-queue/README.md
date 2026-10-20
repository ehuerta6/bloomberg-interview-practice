# Background Job Queue Reference Solution

## What Was Broken

Two workers process the same job after a short delay, and expired work is not reliably reclaimed after a worker disappears. The defect occurs because the workflow does not consistently preserve its key state invariant: expired leases can be reclaimed, stale workers cannot complete or fail another worker’s lease, and retries stop at the configured attempt limit.

## Reproduce and Investigate

From this folder, run `python3 test_job_queue.py`. Compare the reported state with the state stored by the service. Then follow the request through its service, store, and provider or record types. The tests use in-memory state, so each run starts fresh.

## The Fix

The corrected service validates the request before mutation, persists state at the appropriate transition, and handles retries according to the stable event, invoice, transaction, session, or job identifier. A live lease has one owner and excludes other workers until it expires.

## Regression Coverage

The tests cover the reported failure, its successful path, and boundary or replay behavior. They assert persisted records and externally visible effects rather than implementation details.

## Run

```sh
python3 test_job_queue.py
```
