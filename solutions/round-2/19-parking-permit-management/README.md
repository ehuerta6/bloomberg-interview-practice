# Parking Permit Management Reference Solution

## What was wrong

Renewal checked the permit’s `active` flag but did not check whether its inclusive expiration day had already passed. If the expiration sweep had not run, an expired permit could be renewed and made active in practice again.

## Reproduce and investigate

From the starter folder, run:

```sh
python3 test_parking_permits.py
```

Issue a one-day permit on day 1, skip `expire(2)`, and try renewing it on day 2. The starter accepts this renewal even though the permit expired at the end of day 1. Trace the route into `PermitService.renew` and compare its checks with `expire` and the repository’s `active_in_zone` boundary rule.

## Fix

Reject renewal when `expires_day < day`, in addition to checking that the permit is active and the renewal inputs are valid. Because expiration is inclusive, renewal on the expiration day is allowed; renewal on the next day is not. Keep quota counting based on permits active on the requested day.

## Regression tests

- `test_expired_permit_cannot_be_renewed` reproduces renewal after expiry without running the sweep first.
- `test_renewal_extends_from_later_of_today_or_current_expiry` checks extension before and on the inclusive expiry boundary.
- `test_quota_counts_only_unexpired_active_permits` checks zone capacity after existing permits expire.
- Other tests cover the expiration sweep’s boundary and repeat behavior, invalid issuance, freed quota, and invalid renewal without changing the stored date.

## Run the solution tests

```sh
python3 test_parking_permits.py
```
