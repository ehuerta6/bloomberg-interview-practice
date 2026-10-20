# Ticket 19: Parking Permit Management (Easy)

## Ticket

Parking Permit Management needs reliable state transitions.

## Reported symptom

Residents report being denied permits after neighbors’ permits have expired, while a few renewals shift dates backward. The city uses an in-memory permit ledger with inclusive calendar-day expiration.

## Scenario

Compare permit occupancy at the boundary day with the expiration sweep. Then renew permits before and after their expiry and inspect both the date and active state.

## Acceptance criteria

- Enforce per-zone quotas against permits active on the requested day.
- Treat expires_day as inclusive.
- Renew an active permit without shortening its term.
- Do not renew expired or revoked permits.
- Make expiration processing safe to repeat.

## State invariants

- A permit is active through expires_day and inactive afterward.
- Active permits in a zone never exceed the quota on issuance or renewal.
- Renewal never reduces an active permit’s expiration.

## Investigation task

Trace a normal operation, a boundary or failure case, and a repeated request across the route, service, and repository. Explain which state should change, which state must remain untouched, and how your regression tests demonstrate both outcomes. Keep the implementation in memory; no external services or frameworks are required.

## Run the starter tests

```sh
python3 test_parking_permits.py
```

## Exercise folders

- [Starter exercise](../../round-2/19-parking-permit-management/)
- [Reference solution](../../solutions/round-2/19-parking-permit-management/)
