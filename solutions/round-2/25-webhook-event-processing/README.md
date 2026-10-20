# Webhook Event Processing Reference Solution

## Reported behavior

The receiver ignores event sequence ordering, so a delayed payment event can replace a shipped or delivered status. Duplicate event IDs also need a durable in-memory record so retries cannot append history or reapply transitions.

## Reproduce and investigate

From this folder, run:

```sh
python3 test_webhook_events.py
```

Start with `routes.py` to see the request boundary, then follow the call into `service.py` and the in-memory `repository.py`. Reproduce the reported scenario and inspect repository state before and after each operation. The starter tests include examples that pass and regressions that expose the issue.

## Fix

Validate the event before mutation, deduplicate by event ID, and compare each event’s sequence with the most recently applied sequence for that order. Ignore and record stale events so a retry stays idempotent; apply newer events once and retain an ordered history.

## Regression coverage

The solution tests cover valid and invalid requests, state invariants, boundary conditions, repeated operations, and failure paths. They assert the data stored in the repository as well as returned results.

## Run the solution tests

```sh
python3 test_webhook_events.py
```
