# Ticket #16 — Content Moderation Workflow

**Difficulty:** Medium

## Context

You maintain a discussion site's moderation queue. Submitted posts begin
`pending`. A reviewer can approve a post for publication or reject it. The
**audit history** is a saved record of who made an accepted decision and why;
authors may not decide their own posts.

## Practice report

Submit `post-1` as `author-1`, then call
`review("post-1", "author-1", "approve", "self review")`.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Result | `published` | `forbidden` |
| Stored post status | `published` | `pending` |
| Audit events for the post | 1 | 0 |

## Acceptance Criteria

- Only `approve` and `reject` are valid decisions. Unknown posts and unsupported
  decisions return `invalid` without changing posts or audit history.
- Authors cannot review their own posts. A forbidden self-review preserves the
  pending post and adds no audit event.
- An accepted approval changes a pending post to `published`; an accepted
  rejection changes it to `rejected`.
- Each accepted decision appends exactly one audit event with post ID, actor,
  decision, and note.
- A post already decided cannot be decided again. A later review from another
  reviewer returns `conflict` without replacing its status or appending history.

## Out of Scope

Use the existing caller-supplied reviewer identity and in-memory store. Account
roles, automated content analysis, appeals, and concurrent database updates are
outside this ticket.

## Investigation

Trace the self-review report and compare the result with an independent
reviewer's approval and rejection. Add tests that observe both post state and
audit entries after valid, invalid, forbidden, and repeated decisions.

## Starter Code

[View starter code](../../round-2/16-content-moderation-workflow/)

## Reference Solution

[View solution](../../solutions/round-2/16-content-moderation-workflow/)
