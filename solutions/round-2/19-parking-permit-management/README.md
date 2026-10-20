# Parking Permit Management Reference Solution

## Reported behavior

Quota checks include stale permits in some paths and can reject a valid permit after the zone’s old records have expired. Renewal also needs to honor the existing expiration date without creating gaps or resurrecting an expired permit.

## Reproduce and investigate

From this folder, run:

```sh
python3 test_parking_permits.py
```

Start with `routes.py` to see the request boundary, then follow the call into `service.py` and the in-memory `repository.py`. Reproduce the reported scenario and inspect repository state before and after each operation. The starter tests include examples that pass and regressions that expose the issue.

## Fix

Use one consistent definition of active occupancy for quota checks, expire permits only after their final valid day, and extend a still-active permit from the later of today or its current expiration.

## Regression coverage

The solution tests cover valid and invalid requests, state invariants, boundary conditions, repeated operations, and failure paths. They assert the data stored in the repository as well as returned results.

## Run the solution tests

```sh
python3 test_parking_permits.py
```
