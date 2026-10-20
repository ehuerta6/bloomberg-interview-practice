# Notification Deduplication — Reference Solution

## What was broken

The starter stored timestamps by event ID alone, so one recipient's delivery suppressed another recipient's notification. It also moved the timestamp forward for every suppressed retry, turning a fixed deduplication interval into a sliding one. An out-of-order delivery could then rewrite the state used for future decisions.

## Reproduce the issue

Run `python3 deduplicator.py` in the starter folder. Sending event `e1` to `u1` and then `u2` within ten minutes suppresses both. Repeating a retry at minute eight also incorrectly postpones the next allowed send.

## Investigation approach

First define what constitutes a duplicate: both recipient and event identity matter. Then distinguish a successful send from a suppressed attempt. Only successful sends should establish a new window boundary.

## Correction

The reference implementation keys state by `(recipient, event_id)`, validates identities and timezone-aware clocks, and records a timestamp only when it allows delivery. A timestamp that moves backward is suppressed without changing the stored boundary. At exactly ten minutes, the interval has elapsed and delivery is allowed.

## Regression tests

Tests cover recipient isolation, distinct events, the exact time boundary, repeated suppressed retries, out-of-order events, invalid identities, and invalid window/clock configuration.
