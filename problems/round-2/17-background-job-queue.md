# Ticket #17 — Background Job Queue

**Difficulty:** Hard

## Problem

### Reported symptom

Two workers process the same job after a short delay, and expired work is not reliably reclaimed after a worker disappears.

### Scenario

Workers claim jobs using time-limited leases. A worker can crash, retry a failed job, or report completion after its lease expires.

## Acceptance Criteria
- A live lease has one owner and excludes other workers until it expires.
- Expired leases can be reclaimed, stale workers cannot complete or fail another worker’s lease, and retries stop at the configured attempt limit.
- Invalid requests must leave persisted state unchanged.

## State Invariants

Expired leases can be reclaimed, stale workers cannot complete or fail another worker’s lease, and retries stop at the configured attempt limit.

## Investigation

Trace claim, lease expiry, completion, and failure transitions. Use a deterministic clock value to test concurrent claims, stale ownership, and retry exhaustion. Add regression coverage for the behavior you reproduce.

## Starter Code

[View starter code](../../round-2/17-background-job-queue/)

## Reference Solution

[View solution](../../solutions/round-2/17-background-job-queue/)
