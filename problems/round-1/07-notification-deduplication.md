# PR #07 — Notification Deduplication

**Difficulty:** Medium

**PR title:** Suppress repeated notification events

## Summary

A notification worker may retry an event when delivery processing times out. Recipients should still receive distinct events, while retries of a recently accepted notification should be suppressed. You are reviewing `NotificationDeduplicator.should_send(recipient, event_id, now)`, which returns a delivery decision and maintains the time of the last allowed delivery. The default duplicate window is ten minutes.

## Expected behavior
- `should_send(recipient, event_id, now)` returns true for the first delivery and records its time. Both IDs must be nonblank strings and `now` must be timezone-aware.
- Deduplication is scoped to the pair of recipient and event ID; one user's event must not suppress another user's notification.
- Attempts strictly less than ten minutes after the last successful delivery are suppressed. At exactly ten minutes, delivery is allowed.
- A suppressed retry does not move the last-successful timestamp. An out-of-order attempt is suppressed without moving that timestamp backward.
- The configured window must be positive.

## Contract example

Using a fresh deduplicator, process these timezone-aware times on the same day in order:

| Recipient | Event | Time (UTC) | Expected return |
| --- | --- | --- | --- |
| `"u1"` | `"e1"` | `12:00` | `True` |
| `"u2"` | `"e1"` | `12:01` | `True` |
| `"u1"` | `"e1"` | `12:08` | `False` |
| `"u1"` | `"e1"` | `12:10` | `True` |

After the suppressed `12:08` attempt, the last successful time for `u1` and `e1` remains `12:00`. The `12:10` delivery establishes a new successful time.

## Review task

Review how delivery decisions and stored times satisfy recipient isolation and the fixed window. Correct implementation or test discrepancies, then add deterministic cases for the exact boundary, suppressed retries, and out-of-order attempts. Explain the state that each timeline assertion proves.

## Starter Code

[View starter code](../../round-1/07-notification-deduplication/)

## Reference Solution

[View solution](../../solutions/round-1/07-notification-deduplication/)
