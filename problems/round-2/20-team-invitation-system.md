# Ticket #20 — Team Invitation System

**Difficulty:** Easy

## Problem

### Reported symptom

A team admin invites contractors with viewer, editor, or admin access. The team sees an expired link accepted when its cleanup task was delayed, and wants lifecycle rules that do not depend on cleanup timing.

### Scenario

Compare a direct acceptance after expiry with the periodic expiration sweep. Review duplicate detection for pending invitations and membership creation.

## Acceptance Criteria
- Validate email, role, identifier, and positive lifetime.
- Grant team membership only after successful acceptance.
- Reject acceptance at times after expires_at, even if no expiry sweep ran.
- Prevent duplicate live invitations and duplicate membership.
- Allow a new invitation after the prior invitation is expired or cancelled.

## State Invariants
- Only accepted invitations create membership.
- An invitation can leave pending state only once.
- An expired invitation never becomes accepted.
- Each member has one assigned role from the allowed role set.

## Investigation

Trace a pending invitation through acceptance just before, exactly at, and after its expiration time, both with and without an expiration sweep. Check how duplicate pending invites, cancellation, role validation, and repeated acceptance affect membership.

## Starter Code

[View starter code](../../round-2/20-team-invitation-system/)

## Reference Solution

[View solution](../../solutions/round-2/20-team-invitation-system/)
