# Background Job Queue Reference Solution

## What Was Broken

The starter let each caller claim the first nonterminal job, even when another worker held an unexpired lease. It also treated a lease as valid at its exact expiry time. Two workers could consequently own the same job, while an expired worker could still complete or fail it at the boundary.

## Reproduce and Investigate

From this folder, run `python3 test_job_queue.py`. The concurrent-claim test asks two workers to claim at time 100 and checks the lease owner. The reclaim and stale-owner tests use deterministic timestamps around lease expiry; trace `claim`, `complete`, and `fail` while checking the job’s owner, deadline, and attempt count.

## The Fix

`claim` skips a live lease, reassigns an expired lease, and increments attempts on each claim. Completion and failure require the current owner and a lease that has not expired; the deadline itself is expired. A failure requeues the job until the attempt limit, then marks it failed. If a worker disappears on the final attempt, the next claim after expiry marks that job failed instead of leaving it leased forever. Repeated completion of a done job is harmless.

## Regression Tests

The suite covers exclusion of a second worker during a live lease, reclaim after expiry, retry after a reported failure, idempotent duplicate completion, rejection of a stale worker after reassignment, and exhaustion after a final worker disappears.

## Run

```sh
python3 test_job_queue.py
```
