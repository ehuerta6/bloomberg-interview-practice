# Ticket #20 — Team Invitation System

**Difficulty:** Easy

## Context

You maintain invitations to a shared team workspace. A pending invitation
contains an email, a role (`viewer`, `editor`, or `admin`), and an inclusive
expiration time. Acceptance creates membership with that role. A periodic sweep
can mark old invitations expired, but direct acceptance must enforce the lifecycle too.

## Practice report

Create invitation `i2` for `late@example.com` with `now=10` and lifetime `ttl=2`.
Without running the sweep, call `accept("i2", 13)` through the route adapter.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Response status | 409 | 409 |
| Invitation status after rejection | `pending` | `expired` |
| Membership for that email | Absent | Absent |

The reported defect is the saved lifecycle state after an expired acceptance
attempt. For a separate fresh invitation with deadline 12, acceptance at 12 is valid.

## Acceptance Criteria

- Require an unused nonempty invitation ID, an email containing `@`, an allowed
  role, an integer creation time, and a positive integer lifetime. Invalid
  invitations must not create records or membership.
- Do not invite an existing member or create another live pending invitation
  for the same email. A new invitation ID is allowed after expiry or cancellation.
- Accept only a pending invitation at or before its inclusive expiration time.
  Success sets it to `accepted` and creates membership with the invited role once.
- An acceptance attempt after the deadline marks a pending invitation `expired`
  and rejects the request without granting membership, even if no sweep ran.
- Accepted, cancelled, expired, and unknown invitations cannot be accepted again.
  Cancellation can change a pending invitation only once.
- The expiration sweep changes only pending invitations whose deadline has
  passed, returns newly expired IDs, and is safe to repeat.

## Out of Scope

Use the supplied time integers, email checks, and single-workspace repository.
Email delivery, authentication, and replacing the email validator are outside
this ticket.

## Investigation

Trace the direct late-acceptance case and compare it with the sweep. Add tests
before, at, and after the inclusive deadline, including duplicate invitations,
cancellation, and repeated acceptance. Check both saved invitation state and membership.

## Starter Code

[View starter code](../../round-2/20-team-invitation-system/)

## Reference Solution

[View solution](../../solutions/round-2/20-team-invitation-system/)
