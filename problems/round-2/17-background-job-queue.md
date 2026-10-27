# Ticket #17 — Background Job Queue

**Difficulty:** Hard

## Practice Metadata

- **Interview format:** Engineering ticket / existing-code debugging.
- **Primary skills:** lease expiry, stale worker ownership, deterministic state-machine testing.
- **Expected duration:** 50–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Reclaim a job at its exact lease deadline, then prove the former worker cannot alter the new owner's lease.
- **Interviewer evaluation:** Problem decomposition, code navigation, root-cause explanation, incremental implementation, and test evidence. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

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

## Core acceptance criteria

- A live lease excludes another worker. The first claim records one owner,
  increments attempts once, and sets the deadline from the configured lease.
- At the exact deadline the lease is expired and may be reclaimed if attempts
  remain. The new claim updates the owner and increments attempts once.
- The former owner is stale after reassignment. Its completion or failure
  request returns `conflict` and leaves the current owner's lease unchanged.
- `now` is supplied by the caller; tests use fixed values and do not sleep.

## Optional follow-ups

After the expiry and stale-owner regression is complete, discuss terminal
attempts, explicit failure/retry, duplicate completion, or duplicate job IDs.
These behaviors are not prerequisites for the core task.

## Out of Scope

Keep the supplied job store, payloads, and timestamp API. Running the actual job,
database locking, distributed worker coordination, and new configuration
validation are outside this ticket.

## Investigation

Trace claim and reclaim through the stored owner, attempt count, and deadline. Add deterministic tests immediately before and at expiry, then show that the stale worker cannot alter the reassigned lease. Explain which state proves that ownership changed only after expiry.

## Starter Code

[View starter code](../../round-2/17-background-job-queue/)

## Reference Solution

[View solution](../../solutions/round-2/17-background-job-queue/)
