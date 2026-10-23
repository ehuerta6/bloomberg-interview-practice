# Ticket #19 — Parking Permit Management

**Difficulty:** Easy

## Context

You maintain a city's parking-permit ledger. Each zone has a quota of permits
active on a requested day. Days are integers. A permit's `expires_day` is
**inclusive**: a permit expiring on day 3 is valid on day 3 and expired on day 4,
even if the expiration sweep has not updated its stored active flag yet.

## Practice report

Issue permit `a` in `north` on day 1 with duration 1. Its expiration is day 1.
Skip the expiration sweep and request `renew("a", 2, 5)` through the route adapter.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Renewal status | 200 | 409 |
| Stored expiration day | 6 | 1 |

The request must not revive a permit whose inclusive term has ended.

## Acceptance Criteria

- Issuance requires valid IDs, a known zone, integer day and positive integer
  duration, and a new permit ID. Rejected issuance consumes no quota.
- Zone quota counts only permits with an active flag and an expiration on or
  after the requested day. Inactive or expired permits free quota.
- A new term of duration `d` starting on day `t` expires on `t + d - 1`.
- An active, unexpired permit can be extended, including on its final valid day.
  Extension adds the requested duration after its existing term and never shortens
  it. For a permit ending day 3, renewal on day 2 for 2 days ends day 5.
- Reject renewal after expiry or when the permit is inactive, unknown, or the
  renewal input is invalid; preserve its original expiration and ledger state.
- The expiration sweep marks active permits expired only after their final
  valid day and returns newly changed IDs. Repeating it has no further effects.
- Issuance and renewal preserve the per-zone quota invariant.

## Out of Scope

Keep integer day numbering and the existing inactive flag for revocation.
Calendar/time-zone conversion, payments, and a new revocation API are outside
this ticket.

## Investigation

Reproduce renewal without the sweep, then compare the inclusive final day with
the next day. Add tests for quota availability, term extension, invalid renewal,
and a repeated sweep. Assert both returned results and unchanged state after rejection.

## Starter Code

[View starter code](../../round-2/19-parking-permit-management/)

## Reference Solution

[View solution](../../solutions/round-2/19-parking-permit-management/)
