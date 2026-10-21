# PR #07 — Notification Deduplication

**Difficulty:** Medium

**PR title:** Suppress repeated notification events

## Summary

Message delivery can retry an event when a worker times out. This change adds a ten-minute duplicate window so a retry does not send the same notification to a recipient repeatedly.

## Expected behavior
- `should_send(recipient, event_id, now)` returns true for the first delivery and records its time. Both IDs must be nonblank strings and `now` must be timezone-aware.
- Deduplication is scoped to the pair of recipient and event ID; one user's event must not suppress another user's notification.
- Attempts strictly less than ten minutes after the last successful delivery are suppressed. At exactly ten minutes, delivery is allowed.
- A suppressed retry does not move the last-successful timestamp. An out-of-order attempt is suppressed without moving that timestamp backward.
- The configured window must be positive.

## Review task

Follow how keys and timestamps change after both accepted and suppressed attempts. Use a timeline with two recipients, a retry near the window boundary, and an out-of-order event to evaluate whether the state matches “last successful delivery.”

## Starter Code

[View starter code](../../round-1/07-notification-deduplication/)

## Reference Solution

[View solution](../../solutions/round-1/07-notification-deduplication/)
