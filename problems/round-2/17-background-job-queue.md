# Ticket #17 — Background Job Queue

**Difficulty:** Hard

## Context

You maintain background work such as digest emails and image resizing. A
**lease** gives one worker temporary ownership of a job. Another worker may
reclaim the job after that lease expires if the attempt limit allows it.
`now` is a supplied numeric time; no real waiting is needed in tests.

## Practice report

Enqueue `job-1`, then call `claim("worker-a", 100)` with a 30-second lease and
maximum 3 attempts. Immediately call `claim("worker-b", 100)`.

| Observation after the second claim | Current starter | Expected |
| --- | --- | --- |
| Returned job | `job-1` | `None` |
| Stored lease owner | `worker-b` | `worker-a` |
| Attempt count | 2 | 1 |

These are sequential calls at the same supplied time; the report requires no
thread scheduler to reproduce.

## Acceptance Criteria

- A live lease excludes other workers. Each successful claim records one owner,
  increments attempts once, and sets a deadline using the configured lease duration.
- At the exact deadline the lease is expired. An eligible expired job can be
  reclaimed without losing attempt history.
- Only the current owner of an unexpired lease can complete or fail it. A stale
  worker or wrong worker gets `conflict` without changing the current lease.
- Completion makes a job `done`; repeated completion is harmless and a done
  job is never claimed again.
- A reported failure records the error and requeues the job until the attempt
  limit; the final failure is terminal. If the final worker disappears, the
  next claim after expiry marks the exhausted job `failed` without reclaiming it.
- Duplicate job IDs are rejected without replacement. Missing completion and
  invalid ownership requests follow the existing result contract without new jobs.

## Out of Scope

Keep the supplied job store, payloads, and timestamp API. Running the actual job,
database locking, distributed worker coordination, and new configuration
validation are outside this ticket.

## Investigation

Trace claim, completion, failure, and reclaim through stored owner, status,
attempt count, and deadline. Add deterministic tests before and at expiry,
a stale worker after reassignment, a reported retry, and a vanished final worker.
Explain which state proves that only one lease is live.

## Starter Code

[View starter code](../../round-2/17-background-job-queue/)

## Reference Solution

[View solution](../../solutions/round-2/17-background-job-queue/)
