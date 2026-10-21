# Ticket #16 — Content Moderation Workflow

**Difficulty:** Medium

## Problem

### Reported symptom

A post can be approved by its author, and two reviewers can make conflicting decisions while the history shows only the final state.

### Scenario

New posts begin in a review queue. Reviewers may approve or reject pending content, while authors cannot review their own submissions.

## Acceptance Criteria
- Only a pending post can receive one valid review decision.
- Authors cannot review their own posts; every accepted decision appends an actor, decision, and note to the audit history.
- Invalid requests must leave persisted state unchanged.

## State Invariants

Authors cannot review their own posts; every accepted decision appends an actor, decision, and note to the audit history.

## Investigation

Trace role checks and state transitions through the moderation service. Inspect both post state and audit events after forbidden, invalid, and repeated decisions. Add regression coverage for the behavior you reproduce.

## Starter Code

[View starter code](../../round-2/16-content-moderation-workflow/)

## Reference Solution

[View solution](../../solutions/round-2/16-content-moderation-workflow/)
