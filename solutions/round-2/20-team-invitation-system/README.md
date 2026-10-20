# Team Invitation System Reference Solution

## Reported behavior

The service accepts invitations after their deadline unless expiration has already been swept, so behavior depends on a background job having run. Lifecycle transitions also need to prevent duplicate active invitations while allowing a fresh invite after expiry.

## Reproduce and investigate

From this folder, run:

```sh
python3 test_team_invitations.py
```

Start with `routes.py` to see the request boundary, then follow the call into `service.py` and the in-memory `repository.py`. Reproduce the reported scenario and inspect repository state before and after each operation. The starter tests include examples that pass and regressions that expose the issue.

## Fix

Make acceptance enforce the deadline itself, transition an overdue pending invitation to expired, and ensure pending, accepted, cancelled, and expired states have distinct allowed transitions. Preserve the invited role only when acceptance succeeds.

## Regression coverage

The solution tests cover valid and invalid requests, state invariants, boundary conditions, repeated operations, and failure paths. They assert the data stored in the repository as well as returned results.

## Run the solution tests

```sh
python3 test_team_invitations.py
```
