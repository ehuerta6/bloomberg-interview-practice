# Ticket 20: Team Invitation System (Easy)

## Ticket

Team Invitation System needs reliable state transitions.

## Reported symptom

A team admin invites contractors with viewer, editor, or admin access. The team sees an expired link accepted when its cleanup task was delayed, and wants lifecycle rules that do not depend on cleanup timing.

## Scenario

Compare a direct acceptance after expiry with the periodic expiration sweep. Review duplicate detection for pending invitations and membership creation.

## Acceptance criteria

- Validate email, role, identifier, and positive lifetime.
- Grant team membership only after successful acceptance.
- Reject acceptance at times after expires_at, even if no expiry sweep ran.
- Prevent duplicate live invitations and duplicate membership.
- Allow a new invitation after the prior invitation is expired or cancelled.

## State invariants

- Only accepted invitations create membership.
- An invitation can leave pending state only once.
- An expired invitation never becomes accepted.
- Each member has one assigned role from the allowed role set.

## Investigation task

Trace a normal operation, a boundary or failure case, and a repeated request across the route, service, and repository. Explain which state should change, which state must remain untouched, and how your regression tests demonstrate both outcomes. Keep the implementation in memory; no external services or frameworks are required.

## Run the starter tests

```sh
python3 test_team_invitations.py
```

## Exercise folders

- [Starter exercise](../../round-2/20-team-invitation-system/)
- [Reference solution](../../solutions/round-2/20-team-invitation-system/)
