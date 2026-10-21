# Team Invitation System Reference Solution

## What was wrong

`InvitationService.accept` checked the invitation status but accepted a pending invitation even when `now` was later than `expires_at`. That granted team membership from an expired link whenever the background expiration sweep had not run.

## Reproduce and investigate

From the starter folder, run:

```sh
python3 test_team_invitations.py
```

Create an invitation with `now=10` and `ttl=2`, then accept it at time 13 without calling `expire`. Inspect both the invitation status and `repo.members`. Trace the request through `routes.py` and `InvitationService.accept`; compare direct acceptance with the periodic `expire` path.

## Fix

Accept only pending invitations whose inclusive deadline has not passed. When a pending invitation is accepted after its deadline, mark it expired and reject the request without adding a member. Keep acceptance, cancellation, and expiration as one-way lifecycle transitions, and grant the requested role only after acceptance succeeds.

## Regression tests

- `test_invitation_expires_after_inclusive_deadline` accepts at the deadline and rejects after it, checking the expired status.
- `test_role_is_granted_only_after_acceptance` checks that membership is created with the invited role only on acceptance.
- `test_active_pending_invite_prevents_duplicate_but_expired_does_not` covers duplicate live invites and a replacement after expiry.
- Other tests cover cancellation, duplicate membership, invalid roles, cancelled-address reinvitation, and repeat-safe expiration sweeps.

## Run the solution tests

```sh
python3 test_team_invitations.py
```
