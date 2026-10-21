# Ticket #19 — Parking Permit Management

**Difficulty:** Easy

## Problem

### Reported symptom

Residents report being denied permits after neighbors’ permits have expired, while a few renewals shift dates backward. The city uses an in-memory permit ledger with inclusive calendar-day expiration.

### Scenario

Compare permit occupancy at the boundary day with the expiration sweep. Then renew permits before and after their expiry and inspect both the date and active state.

## Acceptance Criteria
- Enforce per-zone quotas against permits active on the requested day.
- Treat expires_day as inclusive.
- Renew an active permit without shortening its term.
- Do not renew expired or revoked permits.
- Make expiration processing safe to repeat.

## State Invariants
- A permit is active through expires_day and inactive afterward.
- Active permits in a zone never exceed the quota on issuance or renewal.
- Renewal never reduces an active permit’s expiration.

## Investigation

Compare quota checks on the inclusive expiration day and the following day. Trace a renewal that would shorten a term, a renewal after expiry, and a repeated expiration sweep; verify that failed operations leave the permit ledger unchanged.

## Starter Code

[View starter code](../../round-2/19-parking-permit-management/)

## Reference Solution

[View solution](../../solutions/round-2/19-parking-permit-management/)
